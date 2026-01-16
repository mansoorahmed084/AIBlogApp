# EBS Storage Guide for Elastic Beanstalk

## Is EBS Storage Free?

**No, EBS storage is NOT free.** You pay per GB per month.

### Current Setup (t3.small)
- **Default EBS Volume**: 8 GB (gp3)
- **Cost**: ~$0.80/month ($0.10 per GB/month for gp3)
- **Problem**: Not enough space for PyTorch (~900MB) + dependencies (~2-3GB total)

## Cost Breakdown

### Option 1: Increase EBS Volume (Recommended)
- **20 GB EBS Volume**: ~$2.00/month
- **30 GB EBS Volume**: ~$3.00/month
- **50 GB EBS Volume**: ~$5.00/month

### Option 2: Use API-Based Transcription (Current Solution)
- **Cost**: FREE (using AssemblyAI free tier)
- **Storage**: No additional EBS needed
- **Trade-off**: Requires internet connection, API rate limits

## How to Increase EBS Volume Size

### Method 1: Via Elastic Beanstalk Console (Easiest)

1. Go to AWS Console → Elastic Beanstalk
2. Select your environment: `ai-blog-env`
3. Go to **Configuration** → **Capacity**
4. Under **Root volume**, increase **Volume size** from 8 GB to **20 GB** (or more)
5. Click **Apply**
6. Wait for environment update (~5-10 minutes)

### Method 2: Via EB CLI

Create `.ebextensions/06_ebs_volume.config`:

```yaml
option_settings:
  aws:autoscaling:launchconfiguration:
    RootVolumeSize: 20
    RootVolumeType: gp3
```

Then deploy:
```bash
eb deploy
```

### Method 3: Via AWS CLI

```bash
# Get your environment's Auto Scaling Group
aws elasticbeanstalk describe-environment-resources \
  --environment-name ai-blog-env \
  --region ap-south-1 \
  --query 'EnvironmentResources.AutoScalingGroups[0].Name' \
  --output text

# Update Launch Configuration (requires recreating)
# This is complex - use Method 1 or 2 instead
```

## After Increasing Storage

Once you increase storage, you can add `openai-whisper` back to `requirements.txt`:

```txt
openai-whisper>=20231117  # Local transcription (requires ~2-3GB disk space)
```

Then redeploy:
```bash
eb deploy
```

## Cost Comparison

| Option | Monthly Cost | Pros | Cons |
|--------|-------------|------|------|
| **Current (8GB, API-based)** | ~$0.80 | Free APIs, no storage increase | Requires internet, API limits |
| **20GB + Local Whisper** | ~$2.00 | No API limits, works offline | Higher cost, slower first load |
| **30GB + Local Whisper** | ~$3.00 | More headroom | Even higher cost |

## Recommendation

**For now**: Keep using API-based transcription (AssemblyAI) - it's FREE and works well.

**If you need local Whisper**: Increase to 20GB EBS volume (~$2/month extra) and add `openai-whisper` back.

## Total Monthly Cost Estimate

### Current Setup (t3.small + 8GB EBS):
- **EC2 Instance (t3.small)**: ~$15/month
- **EBS Storage (8GB)**: ~$0.80/month
- **Data Transfer**: ~$5-10/month
- **Total**: ~$20-25/month

### With 20GB EBS + Local Whisper:
- **EC2 Instance (t3.small)**: ~$15/month
- **EBS Storage (20GB)**: ~$2.00/month
- **Data Transfer**: ~$5-10/month
- **Total**: ~$22-27/month

**Difference**: Only ~$2/month extra for local Whisper support!
