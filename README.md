# Books
Welcome to the "Books" project! This application is designed to help users manage their book inventory.

# Features
### Login screen
![Screenshot_1](https://github.com/idansadi/books/assets/143510244/88ce2c33-0b17-46a0-bf9e-4fa50be93770)

Secure access to your account with a robust login system. 

### Home screen
![Screenshot_2](https://github.com/idansadi/books/assets/143510244/019306ae-770f-4bfc-aa80-0a1f7993b31b)

After logging in to your account, you reach the home page where there are buttons to perform the actions.

### Add books screen
![Screenshot_3](https://github.com/idansadi/books/assets/143510244/6fcb00b7-1517-433c-a347-dcef2cf98044)

Screen for adding a book to inventory. The user can fill in details about the book such as author, year of publication and title. When you click on "Add Book" the book is saved in the database.

### Delete books screen
![Screenshot_4](https://github.com/idansadi/books/assets/143510244/84c937ff-2f2b-49e3-b2e0-62edf5c01341)

Screen for deleting a book from the inventory. The user can delete the books that are in the database. When clicking on "Delete Book" the book is deleted from the database.

### Edit books screen
![Screenshot_5](https://github.com/idansadi/books/assets/143510244/74d8ee71-7f7a-4863-96b0-589352cc60ec)

Screen for editing a book from the inventory. The user can edit the details of the books in the database. When you click on "Edit book" the book is updated in the database.

### Show books screen
![Screenshot_6](https://github.com/idansadi/books/assets/143510244/105b5cfb-1542-405b-b1cf-64256be8116c)

A screen that shows the user the list of books in his inventory.



# Tools I worked with
My project embraces a wide array of technologies and tools to uphold top-notch development standards, continuous integration, and resilient deployment practices. Below is an elaborate breakdown of our technology stack, highlighting our DevOps methodologies.

## Application Development
Python: is a versatile, high-level programming language known for its simplicity and readability. It offers extensive libraries and frameworks, making it ideal for rapid development, data analysis, and web applications.

![Screenshot_6](https://github.com/idansadi/books/assets/143510244/f3b61258-fece-4eb0-8305-aab7502a43cd)

## Database
MongoDB: is a popular NoSQL database management system designed for flexibility, scalability, and performance. It stores data in flexible, JSON-like documents, allowing for seamless integration with modern application development stacks and efficient handling of diverse data types.

![Screenshot_5](https://github.com/idansadi/books/assets/143510244/e1452539-0f18-45bd-8e64-a23959eba212)


## Continuous Integration and Deployment
Jenkins: Serving as an open-source automation server, Jenkins empowers developers globally to consistently build, test, and roll out their software. Jenkins orchestrates our CI/CD pipeline, seamlessly integrating with GitHub to streamline our development lifecycle. In this project, Jenkins is utilized with multibranch pipelines to execute various workflows.

![Screenshot_7](https://github.com/idansadi/books/assets/143510244/638ee405-b107-4ee5-8d44-25b46c3b8e56)

## Containerization and Artifact Storage:

Docker simplifies application deployment by containerizing software and its dependencies, ensuring consistency across diverse environments. DockerHub serves as a centralized repository for Docker images, streamlining image storage, sharing, and collaboration. Leveraging Docker and DockerHub enhances development workflows, promoting scalability and efficiency in application deployment and management.

![Screenshot_1](https://github.com/idansadi/books/assets/143510244/aa98ca3a-c3b3-4dbd-930f-5d84e6463a8d)


# Deployment:

ArgoCD: a GitOps continuous delivery tool designed for Kubernetes, facilitates automated application deployment across multiple environments. It ensures synchronization between Git repositories and production environments, guaranteeing the latest stable application versions are consistently deployed.

![Screenshot_2](https://github.com/idansadi/books/assets/143510244/2592824e-9098-47c3-b0ae-432908f54f7d)


Kubernetes: is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. It provides a resilient infrastructure for running distributed systems, simplifying application deployment and management at scale.

![Screenshot_3](https://github.com/idansadi/books/assets/143510244/b5f42748-66d8-4cf6-9833-0c3f03034882)

## Monitoring
Prometheus: is an open-source monitoring and alerting toolkit designed for reliability and scalability in modern, cloud-native environments. It collects metrics from monitored targets and stores them efficiently, allowing for real-time querying and alerting based on predefined conditions.

![Screenshot_4](https://github.com/idansadi/books/assets/143510244/607d7689-9fbc-419d-9c0d-b80b9e7fb6ac)

# 
Every technology and tool within our arsenal has been meticulously chosen to elevate our development workflow, prioritizing efficiency, dependability, and scalability across our application ecosystem. Our DevOps framework seamlessly integrates into every facet of the application lifecycle, spanning from initial development to deployment, continuous monitoring, and iterative updates. This holistic approach cultivates a culture of perpetual refinement, driving continuous improvement and innovation within our organization.



# How to Install
- First we need to make sure that we have Docker installed and running on our machine.

  If you havent done this yet follow the steps below.
  - If you are Linux users please follow this guide: [Docker for Linux](https://docs.docker.com/engine/install/ubuntu/#installation-methods)
  - If you are Windows or Mac users you need to install Docker Desktop. To install, please choose the link that suits you and follow the guide [Docker for Mac](https://docs.docker.com/desktop/install/mac-install/),   [Docker for Windows](https://docs.docker.com/desktop/install/windows-install/)

- Next step, we need to create a file and give it the name ```docker-compose.yml``` and copy the following content:
```
version: '3'
services:
  web:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    depends_on:
      - mongodb
    environment:
      MONGO_URI: "mongodb://mongodb:27017/books"

  mongodb:
    image: mongo
    ports:
      - "27017:27017"

volumes:
  mongo_data:
```

- Save the file in the directory you choose.

  # How to Access the app
  - Make sure that Docker engine is running on your machine
  - Naviagte to the directory your ```docker-compose.yml``` is loctaed.
  - Open a terminal or command prompt.
 
  - Run the following command:
    
    ```docker-compose up```
    
    When you execute `docker-compose up`, it fetches any required Docker images, establishes containers according to the specifications in the `docker-compose.yml`, and initiates the        services. If the images haven't been previously downloaded, it may require some time for them to be fetched.
  - Run the following command to see the status of the containers:
    ```docker-compose ps```
    This command will display a list of containers managed by Docker Compose along with their status whether they are running or not.

  # Access
  - When the containers are running, you can access the web application by opening a web browser and navigating to [http://localhost:5000](http://localhost:5000)
 
    ## Contributing:
    If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

    ## Contact
    Idan Sadi - idansadi45@gmail.com
