# Cloud Control Sandbox, CCS

Project developed for the research on self-adaptive cloud controllers. 

### Cloud controller      

This component is in charge of the deployment of micro services and taking actions based on the outputs of the algorithm module. 

### Central Unit       

Module containing the scalability algorithms. As an example, the algorithms developed for the article submited to ICCAC 2017 (Extended abstract and poster). 

### Computing Resources       

Web application and load balancer. 
 
### Simulation Unit      

Module in charge of initializing the controller and the Httpmon external application in charge of simulating the workload.

### Workload

32 hours of pre-procesed workload from wikipedia of the extensions the extensions de, es, com and ca.
The full Wikipedia workload is available at http://www.wikibench.eu/?page_id=60

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

# Publication

If you would like to use the presented CloudControlSandbox and/or the experiments (FL, Self-adaptive FL...) please cite the following work:

Jesús Alejandro Cárdenes Cabré, Doina Precup, and Ricardo Sanz. "Horizontal and Vertical Self-Adaptive Cloud Controller with Reward Optimization for Resource Allocation." Cloud and Autonomic Computing (ICCAC), 2017 International Conference on. IEEE, 2017.

Please take into consideration that the presented work in ICCAC 2017 only covers part of my research. Therefore, please let me know if you would like to have a copy of my full master thesis. ( It contains all the information of the cloud control sandbox, the definition of the rewards and the optimal selection of the target thanks to the ORORM for percentage of memory usage.)



### TODO:
Code refactoring of the project.

