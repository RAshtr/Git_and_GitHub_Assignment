# DevOps Project: Flask & MongoDB Atlas Integration

A production-grade Flask web application integrated with MongoDB Atlas, fully containerized using Docker, and automated using GitHub Actions CI/CD pipeline.

## 📁 Repository Structure
├── .github/workflows/
│   └── ci.yml               # Automated CI/CD workflow (Tests + Docker build)
├── templates/
│   ├── form.html            # User submission form with validation alerts
│   └── success.html         # Success redirection view
├── app.py                   # Core application logic & endpoints
├── data.json                # Task 1 JSON data source
├── test_app.py              # Pytest automated test suite
├── Dockerfile               # Container build instructions
├── docker-compose.yml       # Multi-container orchestration
├── requirements.txt         # Pinned production dependencies
├── .env.example             # Template for required environment variables
├── .gitignore               # Security rule to exclude secrets
└── README.md                # Deployment and setup runbook