# Cloud Control Sandbox, CSS

Project developed for the research on self-adaptive cloud controllers. 

### Cloud controller      

This component is in charge of the deployment of micro services and taking actions based on the outputs of the algorithm module. 

### Central Unit       

Module containing the scalability algorithms. As an example, the algorithms developed for the article submited to ICCAC 2017 will be uploaded. 

### Computing Resources       

Web application and load balancer. 
 
### Simulation Unit      

Module in charge of initializing the controller and the Httpmon external application in charge of simulating the workload.

## Dependencies

- Docker SDK for Python: https://github.com/docker/docker-py
- Python Fuzzy Logic library: https://github.com/scikit-fuzzy/scikit-fuzzy
- Httpmon: https://github.com/cloud-control/httpmon

### Docker containers:

##### Web Application
- sudo docker pull chuseuiti/rubos 
(a new version has been created under chuseuiti/rubis, the previous o was a typo. It will be updated on the code)

##### HAProxy Load Balancer:

- sudo docker pull tutum/haproxy
### TODO:

Organize and upload the previously design algorithms.
Refractor the code of the project.
