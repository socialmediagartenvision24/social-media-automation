Social Media Automation Platform

A scalable multi-account social media automation platform for managing, scheduling and publishing video content across Instagram, Facebook and TikTok.

The platform is designed around campaigns, reusable video libraries, automated scheduling, publishing queues and recurring content loops.

🚀 Overview

The system allows you to:

Connect multiple Instagram accounts
Connect multiple Facebook pages/accounts
Connect multiple TikTok accounts
Upload and manage large video libraries
Create reusable content campaigns
Assign campaigns to multiple accounts
Define posting frequency and times
Automatically schedule posts
Automatically publish content
Repeat campaigns after the last video
Pause and resume campaigns
Retry failed publishing jobs
Prevent duplicate publications
Monitor publishing status
View logs and notifications
Track supported analytics

The number of connected accounts is not hardcoded.

🎯 Example Use Case

Example campaign:

Campaign: Fitness Content

Videos:
90

Accounts:
30 Instagram accounts

Posting frequency:
3 videos per day per account

Loop:
Enabled

Timezone:
Europe/Berlin

The system automatically processes the video sequence:

Video 001
Video 002
Video 003
...
Video 090
↓
Video 001
Video 002
Video 003
...

No manual creation of every individual post is required.

🧠 Core Architecture
                         ┌───────────────────┐
                         │     Dashboard     │
                         │                   │
                         │ Accounts          │
                         │ Videos            │
                         │ Campaigns         │
                         │ Calendar          │
                         │ Queue             │
                         │ Analytics         │
                         │ Logs              │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    Backend API    │
                         │      FastAPI      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │     Supabase      │
                         │                   │
                         │ PostgreSQL        │
                         │ Storage           │
                         │ Authentication    │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │  Scheduler /      │
                         │  Publishing Queue │
                         └─────────┬─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
               Instagram       Facebook        TikTok
🏗️ Project Structure
social-media-automation/
│
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── frontend/
│   └── Dashboard application
│
├── backend/
│   └── FastAPI backend
│
├── worker/
│   └── Scheduler and publishing workers
│
├── supabase/
│   ├── migrations/
│   ├── functions/
│   └── seed.sql
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docker/
│   └── Docker configuration
│
└── .github/
    └── workflows/
📋 Features
Accounts

Each social media account is managed independently.

Account information includes:

Platform
Account name
Platform account ID
Connection status
Timezone
Enabled/disabled status
Last successful publication
Last connection check

The architecture supports an arbitrary number of accounts.

🎬 Video Library

The video library provides centralized content management.

Features:

Upload videos
Video previews
File metadata
Duration
File size
Upload status
Active/inactive status
Tags
Campaign assignment

Videos are stored using Supabase Storage.

📦 Campaigns

Campaigns define how content should be distributed.

A campaign contains:

Name
Description
Video collection
Target accounts
Posting frequency
Posting times
Start date
Optional end date
Timezone
Loop configuration
Active/paused status

Example:

Campaign
├── 90 videos
├── 30 Instagram accounts
├── 3 posts/day
├── 09:00
├── 14:00
├── 19:00
└── Loop enabled
🔁 Content Loops

Campaigns can automatically restart after the last video.

Example:

001 → 002 → 003 → ... → 090
                         ↓
001 → 002 → 003 → ... → 090
                         ↓
                        ...

The campaign does not need thousands of future posts stored in the database.

The scheduler generates the required jobs dynamically.

📅 Scheduling

Scheduling supports:

Multiple posts per day
Custom posting times
Account-specific schedules
Campaign-specific schedules
Timezones
Start dates
Optional end dates
Recurring campaigns
Pause/resume

All internal scheduling should use UTC.

User-facing times are displayed using the account or campaign timezone.

⚙️ Publishing Queue

Publishing jobs follow a controlled lifecycle.

pending
   ↓
processing
   ↓
published

Failed jobs:

pending
   ↓
processing
   ↓
failed
   ↓
retry
   ↓
processing

Permanent failures are recorded and displayed in the dashboard.

🛡️ Duplicate Protection

Publishing must be idempotent.

The system stores unique identifiers for publishing jobs and platform publications.

If a worker restarts or an API request times out, the system must determine whether the publication already happened before attempting another publication.

The goal is to prevent accidental duplicate posts.

🔐 Authentication & Security

Authentication is handled through Supabase Auth.

Sensitive credentials must never be committed to Git.

The system must protect:

API keys
OAuth credentials
Access tokens
Refresh tokens
Database credentials
Encryption keys
Supabase service-role credentials

Secrets are provided through environment variables or a secure deployment secret manager.

🌐 Social Platform Integrations

The platform is designed around official platform APIs.

Instagram

Instagram publishing is implemented through the appropriate Meta APIs and permissions available to the connected account.

Facebook

Facebook publishing is implemented through the appropriate Meta APIs and permissions available to the connected page/account.

TikTok

TikTok publishing is implemented through the currently supported TikTok APIs and permissions available to the connected account.

Platform capabilities, publishing limits, account requirements and API permissions must always be validated against the current official API documentation before deployment.

🖥️ Dashboard

The dashboard will contain the following main areas:

Dashboard
│
├── Overview
├── Accounts
├── Videos
├── Campaigns
├── Calendar
├── Publishing Queue
├── Analytics
├── Notifications
├── Logs
└── Settings
📊 Overview

The overview dashboard displays:

Active accounts
Active campaigns
Posts scheduled
Posts published today
Failed posts
Upcoming posts
Worker status
Platform connection status
👤 Account Manager

The account manager allows users to:

Connect accounts
Disconnect accounts
Enable accounts
Disable accounts
View connection status
View account timezone
View recent publications
🎥 Media Library

The media library allows users to:

Upload videos
Preview videos
Search videos
Filter videos
Tag videos
Select multiple videos
Disable videos
Delete videos
📦 Campaign Builder

A campaign can be created using:

1. Select videos
2. Select accounts
3. Define posting frequency
4. Define posting times
5. Select timezone
6. Select start date
7. Configure loop
8. Activate campaign
🗓️ Calendar

The calendar displays scheduled content.

Users can:

View upcoming posts
Filter by account
Filter by platform
Filter by campaign
Pause campaigns
Resume campaigns
Inspect individual jobs
📤 Publishing Queue

The queue displays:

Pending jobs
Processing jobs
Published jobs
Failed jobs
Retry count
Error information
Publication timestamp
🔔 Notifications

The system can notify the user about:

Failed posts
Expired connections
Authentication problems
Worker problems
Platform API errors
Campaign problems
❤️ Health Monitoring

The system should monitor:

Backend       🟢
Worker        🟢
Database      🟢
Storage       🟢
Instagram     🟢
Facebook      🟢
TikTok        🟢

The dashboard should make infrastructure and platform problems visible.

🧱 Technology Stack
Frontend
Next.js
TypeScript
Tailwind CSS
Supabase Auth
Backend
Python
FastAPI
Pydantic
Database
Supabase
PostgreSQL
Storage
Supabase Storage
Worker
Python
Scheduler
Publishing queue
Retry handling
Infrastructure
Docker
GitHub Actions
🗄️ Data Architecture

The database will contain entities for:

Users
Social Accounts
Platform Connections
Videos
Campaigns
Campaign Videos
Schedules
Scheduled Posts
Post Attempts
Notifications
Audit Logs

Relationships will be designed so that one campaign can contain many videos and target many accounts.

🔄 Publishing Flow

The expected publishing flow is:

User creates campaign
        ↓
Campaign saved in Supabase
        ↓
Scheduler evaluates campaign
        ↓
Next required post is calculated
        ↓
Publishing job created
        ↓
Job enters queue
        ↓
Worker receives job
        ↓
Video retrieved from Storage
        ↓
Platform adapter called
        ↓
Official platform API
        ↓
Publication result received
        ↓
Database updated
        ↓
Log created
        ↓
Next job scheduled
🔁 Retry Flow

If a temporary error occurs:

Publish
   ↓
Error
   ↓
Retry #1
   ↓
Error
   ↓
Retry #2
   ↓
Error
   ↓
Retry #3
   ↓
Permanent failure

Retry behavior will depend on the type of platform error.

Permanent authentication or permission errors should not be blindly retried indefinitely.

🌍 Timezone Handling

The system stores timestamps internally in UTC.

Accounts and campaigns can have their own timezone.

Example:

Account timezone:
Europe/Berlin

Posting time:
18:00

Internal scheduling:
UTC

This prevents scheduling problems when daylight-saving time changes.

🧪 Testing

The project will contain:

Unit Tests

Testing individual services and business logic.

Integration Tests

Testing communication between:

Backend
Database
Storage
Worker
End-to-End Tests

Testing complete flows such as:

Upload video
→ Create campaign
→ Schedule post
→ Queue job
→ Publish
→ Record result
🐳 Docker

Docker will be used to run the major services consistently.

Planned services:

frontend
backend
worker

Supabase can be used as the hosted backend infrastructure or run locally during development when required.

🚀 Deployment

The final production deployment will contain:

Frontend
    ↓
Backend API
    ↓
Worker
    ↓
Supabase
    ↓
Social Platform APIs

The worker must run continuously in production.

🔒 Production Requirements

Before production deployment, the following must be verified:

API credentials
OAuth flows
Platform permissions
Account permissions
Rate limits
Video requirements
Retry behavior
Duplicate protection
Worker restart behavior
Database backups
Storage configuration
Monitoring
Error notifications
🛣️ Development Roadmap
Phase 1 — Foundation

Repository structure

Documentation

Environment configuration

Docker configuration

Phase 2 — Database

Supabase project

Database schema

Row Level Security

Storage buckets

Database indexes

Seed data

Phase 3 — Backend

FastAPI application

Authentication

Account API

Video API

Campaign API

Scheduling API

Queue API

Logs API

Phase 4 — Dashboard

Login

Overview

Account management

Video library

Campaign builder

Calendar

Queue

Logs

Notifications

Settings

Phase 5 — Automation

Scheduler

Queue processing

Retry system

Duplicate protection

Campaign loops

Worker monitoring

Phase 6 — Platform Integrations

Instagram

Facebook

TikTok

Phase 7 — Production

Automated tests

Docker deployment

Monitoring

Error alerts

Database backups

Production security review

Load testing

⚠️ Important

This application must use the official APIs and permitted automation mechanisms of each social media platform.

The system must not rely on:

Browser automation to bypass platform restrictions
Credential sharing
CAPTCHA bypasses
Rate-limit bypasses
Unauthorized API endpoints

Platform-specific functionality depends on the permissions and capabilities provided by each platform.

📌 Current Status

The project is currently in the foundation phase.

The next implementation step is the complete Supabase database schema.

License

Private project.

All rights reserved.
