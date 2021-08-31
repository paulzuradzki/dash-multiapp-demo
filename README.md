<!-- TODO: add instructions for alternative to `pip install` from the web (install from wheels/zip file instead) -->

# Python Web Application Server Setup for Production

## Contents
* [Terms](#terms)
* [Assumptions](#assumptions)
* [Steps](#steps)
    * [Initial user setup for server](#initial-user-setup-for-server)
    * [Secure the server](#secure-the-server)
    * [Install server dependencies](#install-server-dependencies)
    * [Install your web application and Python dependencies](#install-your-web-application-and-python-dependencies)
    * [`gunicorn` - set up the Python WSGI (Web Service Gateway Interface) server](#gunicorn-\--set-up-the-python-wsgi-web-service-gateway-interface-server)
    * [`supervisor` - set up process control](#supervisor-\--set-up-process-control)
    * [`nginx` - set up the web server](#nginx-\--set-up-the-web-server)
    * [HTTPS and SSL Cert Setup](#https-and-ssl-cert-setup)

## Terms
* `supervisor` enables processes to run as background services and restart when the server reboots
* `gunicorn` is a Python WSGI (web server gateway interface) server which interfaces between our web app and the web server
    * a WSGI container is a separate running process that runs on a different port than your web server 
    * your web server is configured to pass requests to the WSGI container which runs your web application, then it passes the response (in the form of HTML) back to the requester
* `nginx` (alternative to Apache HTTP server) is a web server that responds directly to client requests

## References
* https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04
* https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux
* https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04
* https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04

## Assumptions
* You have access to a server
    * You have a server (Ubuntu 20.04) to which you can SSH into
        * Your security settings likely need to be modified to permit your IP address for SSH access
    * You have access to a root/superuser private key or password on the server
        * e.g., for AWS EC2, you should have a private key file
    * Set up to use Amazon EC2 - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html
* Beginner familiarity with git and Linux commands. Below are resources.
    * Linux Journey - https://linuxjourney.com/
    * Git and GitHub for Python Developers - https://realpython.com/python-git-github-intro/

___
# Steps

## Initial user setup for server
* Create a user and grant admin rights
* Setup SSH for super user
* I use the username `pz-dev` throughout the ReadMe demo. Modify the name to your own choosing.
    * Note: if you use a different username, make sure that you are using the correct username in config files and terminal commands throughout

Create a user and grant admin rights
```
$ ssh root@your_server_ip       # connect to host; you may need to replace "root" with "ubuntu"
$ adduser pz-dev                # add user
$ usermod -aG sudo pz-dev       # grant admin rights
$ su pz-dev                     # switch to new user
$ mkdir ~/.ssh                  # make this directory in USER home (not root) if it does not exists
$ touch ~/.ssh/authorized_keys                                  # make this file
$ echo {YOUR CLIENT HOST PUBLIC KEY} >> ~/.ssh/authorized_keys  # append public key info to file 
$ chmod 600 ~/.ssh/authorized_keys                              # restrict permissions to file
```

## Secure the server
* Disable root login
* Disable password authentication
* Set up firewall and rules

Modify the sshd_config file (e.g., using vim)
```
# /etc/ssh/sshd_config
PermitRootLogin no              # Disable root logins
PasswordAuthentication no       # Disable password logins
```

For the firewall, enable SSH, HTTPS, and HTTP
```
$ sudo apt-get install -y ufw
$ sudo ufw allow ssh
$ sudo ufw allow http
$ sudo ufw allow 443/tcp
$ sudo ufw --force enable
$ sudo ufw status
```

## Install server dependencies
```
$ sudo apt-get -y update
$ sudo apt-get -y install python3 python3-venv python3-dev
$ sudo apt-get -y install supervisor nginx git
```

## Install your web application and Python dependencies
```
# get application from GitHub
$ git clone https://github.com/paulzuradzki/dash-multiapp-demo.git

# create a virtual environment and install Python dependencies specified in requirements.txt
$ cd dash-multiapp-demo
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt

# also install gunicorn (WSGI server)
$ pip install gunicorn
```


## `gunicorn` - set up the Python WSGI (Web Service Gateway Interface) server
* This command manually runs the app from the gunicorn WSGI server
* The FLASK_APP environment variable is for using `flask run` commands; however, the Flask built-in server is not meant for production
* gunicorn WSGI server is one step closer to production. WSGI server is an interface between our Python app and the web server that handles requests (nginx or Apache HTTP)
* If the server were to reboot, we don't want to have to do this manually, so we will automate the restart using `supervisor` in a later step
* `-b localhost:8000` tells WSGI on what port we will run the app
* The app will run on 8000. A web server (nginx) will directly receive HTTPS/HTTP requests on 443/80 and forward them to gunicorn WSGI server and the Python application  
* for `index:server`, `index` is the name of the Python module file containing the `server` variable. This may differ from app to app depending on how where you've created the server variable. E.g., some tutorials online may show something like `app:app` or `app:app.server`. 
* gunicorn must be called from applicaton project directory; else, provide the full path 

```
echo "export FLASK_APP=index.py" >> ~/.profile
(venv) $ gunicorn -b localhost:8000 -w 4 index:server

# or
(venv) /home/pz-dev/dash-multiapp-demo/venv/bin/gunicorn -b localhost:8000 -w 4 index:server
```


## `supervisor` - set up process control
* supervisor makes the app/gunicorn restart in case the server is rebooted; this avoids manual intervention
* note program name (`[program:index]`) if you change the app structure in Flask/Dash
* the command line is what we would 
```
# /etc/supervisor/conf.d/dash-app.conf
[program:index]
command=/home/pz-dev/dash-multiapp-demo/venv/bin/gunicorn -b localhost:8000 -w 4 index:server
directory=/home/pz-dev/dash-multiapp-demo
user=pz-dev
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

Reload supervisor after creating supervisor configuration file
```
$ sudo supervisorctl reload
```

## `nginx` - set up the web server 
Make self-signed cert for testing
```
openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
  -keyout certs/key.pem -out certs/cert.pem
```

Remove default nginx site
```
$ sudo rm /etc/nginx/sites-enabled/default
```

Create an nginx web server configuration file for the application
```
# /etc/nginx/sites-enabled/dash-app

server {
    # listen on port 80 (http)
    listen 80;
    server_name _;
    location / {
        # redirect any requests to the same URL but on https
        return 301 https://$host$request_uri;
    }
}
server {
    # listen on port 443 (https)
    listen 443 ssl;
    server_name _;

    # location of the self-signed SSL certificate
    ssl_certificate /home/pz-dev/repos/dash-multiapp-demo/certs/cert.pem;
    ssl_certificate_key /home/pz-dev/repos/dash-multiapp-demo/certs/key.pem;

    # write access and error logs to /var/log
    access_log /var/log/dash_app_access.log;
    error_log /var/log/dash_app_error.log;

    location / {
        # forward application requests to the gunicorn server
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        # handle static files directly, without forwarding to the application
        alias /home/pz-dev/repos/dash-multiapp-demo/app/static;
        expires 30d;
    }
}

```

Restart Nginx webserver after creating 
```
sudo service nginx reload
```

## HTTPS and SSL Cert Setup
* See instructions via Digital Ocean for how to set up signed SSL certificates using LetsEncrypt
* This enables HTTPS for production deployment
* Without HTTPS, the browser will show a warning and may prevent the user from accessing the site
* For corporate deployments, a networking or system admin may have to provide the certificates
* You will have to modify the nginx configuration above to re-point the `ssl_certificate` and `ssl_certificate_key` file paths
* Link: https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04