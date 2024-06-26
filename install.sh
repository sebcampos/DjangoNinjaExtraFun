#!/bin/bash

set_up_dependencies()
{
	# TODO add needrestart flag to bypass restart prompt https://askubuntu.com/questions/1367139/apt-get-upgrade-auto-restart-services
	NEEDRESTART_MODE=a apt-get dist-upgrade --yes

	# install pyenv dependencies
	apt update
	apt install \
	    build-essential \
	    curl \
	    libbz2-dev \
	    libffi-dev \
	    liblzma-dev \
	    libncursesw5-dev \
	    libreadline-dev \
	    libsqlite3-dev \
	    libssl-dev \
	    libxml2-dev \
	    libxmlsec1-dev \
	    llvm \
	    make \
	    tk-dev \
	    wget \
	    xz-utils \
	    zlib1g-dev

	# install rust
	# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh  # may need restart


	# install nginx, rabbitmq and postgres dependencies
	apt-get install nginx  -y 
	apt-get install postgresql postgresql-contrib  -y 
	apt-get install rabbitmq-server  -y 
	apt-get install libpq-dev  -y 
}

add_pyenv_to_launching_user()
{
	echo "Setting up pyenv ..."
	cd "$HOME"
	curl https://pyenv.run | bash
	echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> "$HOME/.bashrc"
	echo 'eval "$(pyenv init --path)"' >> "$HOME/.bashrc"
	echo 'eval "$(pyenv virtualenv-init -)"' >> "$HOME/.bashrc"
}

set_up_postgres()
{
	echo "Setting up Postgres"
	psql -c "CREATE DATABASE $DB_NAME;"
	psql -c "CREATE USER $USER_NAME with PASSWORD '$PASSWORD';"
	psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $USER_NAME;"
	psql -c "ALTER DATABASE $DB_NAME OWNER TO $USER_NAME;"
	psql -c "GRANT CREATE ON SCHEMA public TO $USER_NAME;"
	psql -c "ALTER USER $USER_NAME CREATEDB;"

}

set_up_rabbitmq()
{
	echo "Setting up rabbitmq ..."
	rabbitmqctl add_user $USER_NAME $PASSWORD
	rabbitmqctl set_user_tags $USER_NAME administrator
	rabbitmqctl add_vhost $VHOST
	rabbitmqctl set_permissions -p $VHOST $USER_NAME ".*" ".*" ".*"
}

set_up_python_with_pyenv()
{
	 echo "Installing python and python virtual env, this may take a while ..."
	 $HOME/.pyenv/bin/pyenv install $PYTHON_VERSION
	 $HOME/.pyenv/bin/pyenv virtualenv $PYTHON_VERSION $PYTHON_VIRTUALENV
	 $HOME/.pyenv/versions/$PYTHON_VIRTUALENV/bin/pip install -r requirements.txt
}


export USER_NAME="sebash"
export PASSWORD="Lkdfgieowg382"
export DB_NAME="apidb"
export VHOST="apivhost"
export PYTHON_VERSION="3.12.2"
export PYTHON_VIRTUALENV="RestAPI"
export GROUP_NAME="djangoapi"

# install dependencies with apt
set_up_dependencies

# install and configure pyenv for specified user
export -f add_pyenv_to_launching_user
su $USER_NAME -c "add_pyenv_to_launching_user"

# set up postgres
export -f set_up_postgres
su postgres -c "set_up_postgres"

# set up rabbitmq broker
export -f set_up_rabbitmq
set_up_rabbitmq

# set up python and virtualenv
export -f set_up_python_with_pyenv
su $USER_NAME -c "set_up_python_with_pyenv"


mkdir /var/www
groupadd $GROUP_NAME
chgrp $GROUP_NAME /var/www
chmod g+rwx /var/www
usermod -a -G $GROUP_NAME $USER_NAME
