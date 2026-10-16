# Student Management DevOps Project

**Student:** Sarvesh Nage  
**Stack:** Python, Flask, Pytest, Git/GitHub, Docker, Jenkins, Kubernetes/Minikube

A small REST API for student records and academic marks, structured to demonstrate a basic CI/CD workflow.

## Features
- `GET /` — application metadata
- `GET /health` — health check
- `GET /students` — list students
- `POST /students` — create a student (`student_id`, `name`, `course`)
- `GET /students/<student_id>` — retrieve a student
- `PUT /students/<student_id>/marks` — set marks from 0 to 100
- `DELETE /students/<student_id>` — delete a student

> Data is held in memory for demonstration. It resets when the app restarts; use a database for persistent production data.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python run.py
```
Open `http://127.0.0.1:5000/health`.

## Test
```bash
pytest -q
```

## Try the API
Create a record:
```bash
curl -X POST http://127.0.0.1:5000/students \\
  -H 'Content-Type: application/json' \\
  -d '{"student_id":"S001","name":"Asha Patil","course":"BTech AIML"}'
```
Record marks:
```bash
curl -X PUT http://127.0.0.1:5000/students/S001/marks \\
  -H 'Content-Type: application/json' -d '{"marks":88}'
```

## Docker
```bash
docker build -t student-management:v1 .
docker run --rm -p 5000:5000 --name student-management student-management:v1
```

## Kubernetes / Minikube
Build the image in Minikube's Docker environment or load it into Minikube, then:
```bash
kubectl apply -f k8s/
kubectl rollout status deployment/student-management
kubectl get pods,services
minikube service student-management
```
The NodePort service uses port `30080`. For a local Minikube image, run `eval $(minikube docker-env)` before `docker build`, or use `minikube image load student-management:v1` after building the image.

## Jenkins CI
Create a Pipeline job pointing to this GitHub repository and set **Script Path** to `Jenkinsfile`. The agent needs Python 3, permission to create a virtual environment, and Docker CLI/daemon access. The pipeline checks out the repository, installs dependencies, runs Pytest and archives JUnit test results, then builds a Docker image. A Jenkins user added to the Docker group effectively has root-equivalent host access; grant that access only to a trusted Jenkins instance.

## Suggested GitHub setup
1. Create/choose the repository `SarveshX28/student-management-devops`.
2. Upload the project files without `.venv`, `venv`, or secrets.
3. Confirm `main` contains `Jenkinsfile`, `Dockerfile`, `app/`, `tests/`, and `k8s/`.
4. Configure Jenkins with the repository URL and run **Build Now**.

## Evidence note
The accompanying evidence report documents the local source files and test execution performed for this prepared package. It does not claim that the user's EC2 instance, remote GitHub push, Jenkins UI, or Kubernetes cluster was accessed or successfully deployed from this environment.
