#!/usr/bin/env python3
"""collect_metrics.py

Collect EC2 CPU utilization metrics for running instances over a period and output CSV with recommendations.
"""
import boto3
import datetime
import argparse
import csv
from botocore.config import Config

cfg = Config(retries={'max_attempts': 5, 'mode': 'standard'})

def get_instances(ec2):
    paginator = ec2.get_paginator('describe_instances')
    for page in paginator.paginate(Filters=[{'Name':'instance-state-name','Values':['running']} ]):
        for r in page['Reservations']:
            for i in r['Instances']:
                yield i

def avg_cpu(cloudwatch, instance_id, days=7):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=days)
    resp = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name':'InstanceId','Value':instance_id}],
        StartTime=start,
        EndTime=end,
        Period=3600,
        Statistics=['Average']
    )
    points = [p['Average'] for p in resp.get('Datapoints',[])]
    if not points:
        return 0.0
    return sum(points)/len(points)

def get_price(pricing, instance_type, region):
    # Best-effort price lookup using AWS Pricing API in us-east-1 region
    try:
        filters = [
            {'Type':'TERM_MATCH','Field':'instanceType','Value':instance_type},
            {'Type':'TERM_MATCH','Field':'location','Value':region}]
        resp = pricing.get_products(ServiceCode='AmazonEC2', Filters=filters, MaxResults=1)
        price_item = resp['PriceList'][0]
        # pricing response is complex — for POC we skip parsing and return None
        return None
    except Exception:
        return None

def recommend(instance_type, avg_cpu):
    # simple rules for demo
    if avg_cpu < 10:
        return 'downsize'
    if avg_cpu > 80:
        return 'upgrade'
    return 'no-change'

def main():
    parser = argparse.ArgumentParser(description='Collect EC2 metrics and recommend rightsizing')
    parser.add_argument('--days', type=int, default=7)
    parser.add_argument('--output', type=str, default='reports/cost_optimization_report.csv')
    parser.add_argument('--region', type=str, default=None)
    args = parser.parse_args()

    session = boto3.Session(region_name=args.region)
    ec2 = session.client('ec2', config=cfg)
    cw = session.client('cloudwatch', config=cfg)
    pricing = boto3.client('pricing', region_name='us-east-1', config=cfg)

    rows = []
    for inst in get_instances(ec2):
        iid = inst['InstanceId']
        itype = inst.get('InstanceType','unknown')
        az = inst.get('Placement',{}).get('AvailabilityZone','')
        avg = round(avg_cpu(cw, iid, args.days),2)
        rec = recommend(itype, avg)
        price = get_price(pricing, itype, args.region or 'US East (N. Virginia)')
        rows.append({'InstanceId': iid, 'InstanceType': itype, 'AZ': az, 'AvgCPU': avg, 'Recommendation': rec, 'EstimatedHourlyPrice': price})

    # write CSV
    out = args.output
    with open(out, 'w', newline='') as csvfile:
        fieldnames = ['InstanceId','InstanceType','AZ','AvgCPU','Recommendation','EstimatedHourlyPrice']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Wrote report to {out}")

if __name__ == '__main__':
    main()

