# nexus1
soical profiling

# Advanced Prompt for AI Coder

# Build an Intelligence-Grade OSINT & Digital Footprint Investigation Platform

You are a **principal intelligence systems architect, OSINT engineer, data scientist, and distributed systems developer**.

Design and implement a **next-generation Open Source Intelligence (OSINT) platform** capable of performing **deep digital footprint analysis on individuals, organizations, domains, and digital identities using strictly publicly available information**.

The platform must operate like a **professional investigation environment used by cybersecurity teams, investigative journalists, fraud analysts, and threat intelligence analysts**.

The system must support **large-scale automated intelligence gathering, AI-driven correlation, entity resolution, and visual investigation workflows**.

---

# Core System Goals

The system must be able to start with **minimal information** and autonomously expand intelligence.

Example inputs:

* username
* name
* email
* phone number
* image
* social media profile
* domain
* company name

From this, the system must build a **complete digital footprint graph**.

---

# Intelligence Disciplines to Implement

The system must combine multiple OSINT intelligence domains.

SOCMINT
Social media intelligence

GEOINT
Geolocation intelligence

IMINT
Image intelligence

SIGINT-like public signals (public metadata)

WEBINT
Open web intelligence

RELINT
Relationship intelligence

BEHAVINT
Behavioral intelligence

---

# Architecture Overview

The platform must follow **distributed intelligence architecture**.

Core layers:

1 Data Acquisition Layer
2 Intelligence Processing Layer
3 Correlation & Entity Resolution Layer
4 Knowledge Graph Layer
5 AI Analysis Layer
6 Investigation Interface
7 Reporting & Export Layer

---

# 1 Data Acquisition Layer

Build a **modular OSINT collector framework**.

Each source must be a **plugin**.

Collectors must support:

* scraping
* APIs
* RSS feeds
* open databases
* search engine queries

Collectors should operate asynchronously.

Frameworks:

Python
Scrapy
Playwright
Selenium (when needed)

Features:

rate limiting
proxy support
captcha detection
retry logic

---

# 2 Global Source Coverage

The platform must support discovery from the widest range of **public data sources**.

### Social Media Platforms

Include collectors for:

* Facebook
* Instagram
* X
* LinkedIn
* TikTok
* Reddit
* YouTube
* Snapchat public profiles
* Telegram public groups
* Discord public servers
* Pinterest
* Tumblr
* Threads

---

### Developer Platforms

* GitHub
* GitLab
* Bitbucket
* StackOverflow

---

### Public Web Data

* blogs
* forums
* comment sections
* review platforms
* paste sites
* news comments

---

### Domain Intelligence

* WHOIS
* DNS records
* domain history
* SSL certificates
* subdomains

---

### Breach Intelligence

Public datasets such as:

credential leak repositories
public breach archives

---

### Search Engine Intelligence

Use automated queries on

Google
Bing
DuckDuckGo

To discover:

* mentions
* cached content
* archived pages

---

# 3 Identity Resolution Engine

One of the most important components.

Goal: determine whether accounts belong to the same individual.

Techniques:

username similarity
avatar similarity
bio keyword matching
location similarity
follower overlap
posting patterns

Use **machine learning scoring**.

Output:

identity confidence score.

---

# 4 Knowledge Graph Engine

Store all discovered intelligence in a **graph database**.

Technology

Neo4j

Entities:

person
account
organization
email
phone
domain
location
image
event

Relationships:

owns
works_for
follows
mentioned_by
posted_from
related_to

This allows complex queries like:

"Show all accounts related to this identity within two hops."

---

# 5 Image Intelligence System

Implement a complete **image OSINT module**.

Capabilities:

reverse image search
face similarity detection
duplicate image detection
landmark recognition
logo detection
object detection

Tools:

OpenCV
DeepFace
YOLO models

Also extract EXIF metadata.

---

# 6 Geolocation Intelligence

Determine location using multiple signals.

Sources:

EXIF coordinates
post geotags
landmarks in images
language usage
timezone activity
local events mentioned

Generate:

probable city
travel history
movement timeline

Visualize using maps.

---

# 7 Social Network Graph Analysis

Construct relationship graphs.

Nodes:

accounts
people
organizations

Edges:

followers
mentions
replies
tags
shared groups

Run graph algorithms:

community detection
centrality analysis
influence scoring

---

# 8 Behavioral Intelligence

Analyze posting behavior.

Detect:

active hours
sleep cycle
weekend vs weekday activity
platform preference
content categories

Build behavioral fingerprint.

---

# 9 Content Intelligence (NLP)

Process all text data.

Extract:

topics
sentiment
political indicators
interests
languages used

Libraries:

spaCy
transformer models

Use topic modeling such as LDA.

---

# 10 Temporal Intelligence

Create event timeline.

Examples:

account creation
profile changes
major posting spikes
travel events

Provide interactive timeline visualization.

---

# 11 AI Correlation Engine

Use machine learning to detect hidden connections.

Examples:

two accounts sharing same images
similar writing style
identical usernames across platforms
overlapping followers

Output probable identity clusters.

---

# 12 Investigation Workspace

Create an investigator interface similar to professional tools.

Features:

case management
target profiles
notes
evidence tagging
timeline exploration
relationship graphs

---

# 13 Visualization System

Provide powerful visual tools.

Visualizations include:

relationship network graphs
geographic maps
timeline charts
activity heatmaps
content topic graphs

Libraries:

D3.js
Mapbox
Cytoscape.js

---

# 14 Automated Intelligence Agents

Build autonomous scanning agents.

Capabilities:

continuous monitoring
watchlists
alerts on new posts
alerts on new accounts discovered

Queue system:

Celery + Redis.

---

# 15 AI Report Generator

Automatically generate professional reports.

Sections:

target summary
discovered accounts
relationship network
geolocation findings
image intelligence
risk indicators

Formats:

PDF
HTML
JSON

---

# Backend Architecture

Language

Python

Framework

FastAPI

Key services

collector service
analysis service
graph service
report service

---

# Databases

PostgreSQL
ElasticSearch
Neo4j
Redis

---

# Frontend

Build intelligence dashboard.

Framework

React or Next.js

Modules

search interface
case workspace
map explorer
graph explorer
media viewer

---

# Security

Implement:

role based access
audit logging
data encryption
API authentication

---

# Scalability

Support large investigations.

Use

Docker
Kubernetes

Allow distributed workers.

---

# Plugin System

Allow developers to add:

new OSINT sources
new AI models
new analysis modules

---

# Deliverables

The AI coder must produce:

complete source code
database schema
deployment scripts
API documentation
sample dataset
example investigation report

---

# Performance Targets

System should be capable of:

scanning hundreds of platforms
processing thousands of profiles
building millions of graph relationships

---

# Legal Requirement

The system must:

use only public data
respect platform policies
avoid bypassing authentication

---

# Final Goal

Build an **intelligence-grade OSINT investigation system** that enables analysts to map **complete digital identities and social networks from open data sources**.


