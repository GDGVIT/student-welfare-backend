<p align="center">
<a href="https://dscvit.com">
	<img width="400" src="https://user-images.githubusercontent.com/56252312/159312411-58410727-3933-4224-b43e-4e9b627838a3.png#gh-light-mode-only" alt="GDSC VIT"/>
</a>
	<h2 align="center"> Student Welfare Backend </h2>
	<h4 align="center"> API for the student welfare website and app <h4>
</p>

---
[![Join Us](https://img.shields.io/badge/Join%20Us-Developer%20Student%20Clubs-red)](https://dsc.community.dev/vellore-institute-of-technology/)
[![Discord Chat](https://img.shields.io/discord/760928671698649098.svg)](https://discord.gg/498KVdSKWR)

[![DOCS](https://img.shields.io/badge/Documentation-see%20docs-green?style=flat-square&logo=appveyor)](INSERT_LINK_FOR_DOCS_HERE) 
  [![UI ](https://img.shields.io/badge/User%20Interface-Link%20to%20UI-orange?style=flat-square&logo=appveyor)](INSERT_UI_LINK_HERE)


## Table of Contents
- [Key Features](#key-features)
	- [Users](#users)
	- [Clubs](#clubs)
	- [Events](#events)
	- [Notifications](#notifications)
- [Usage](#usage)
	- [Spin up all the containers](#spin-up-all-the-containers)
	- [Migrate changes to the database](#migrate-changes-to-the-database)
	- [Create a superuser](#create-a-superuser)
	- [Other management commands](#other-management-commands)
	- [Stop all the containers](#stop-all-the-containers)
	- [View logs](#view-logs)
	- [View logs for a specific container](#view-logs-for-a-specific-container)
	- [Run any command inside a container](#run-any-command-inside-a-container)
- [Developer](#developer)

<br>

## Key Features
### Users
- [x] Custom User Model for Admin, Faculty and Student
- [x] JWT based user authentication
- [x] Email OTP Verification
- [x] User Bulk Upload

### Clubs
- [x] CRUD operations for clubs
- [x] Bulk Upload for clubs from CSV
### Events
- [x] CRUD operations for events
- [x] Bulk Upload for events from CSV

### Notifications
- [x] Push notifications


<br>

## Usage

Here are some commonly used commands -
### Spin up all the containers
```bash
./sw.sh up -d --build
```	


### Migrate changes to the database
```bash
./sw.sh run --rm django python manage.py migrate
```

### Create a superuser
```bash
./sw.sh run --rm django python manage.py createsuperuser
```

### Other management commands
```bash
./sw.sh run --rm django python manage.py <command>
```

### Stop all the containers
```bash
./sw.sh down
```

### View logs
```bash
./sw.sh logs -f
```

### View logs for a specific container
```bash
./sw.sh logs -f <container_name>
```
  
### Run any command inside a container
```bash
./sw.sh run --rm <container_name> <command>
```

For windows, use `sw.cmd` instead of `sw.sh`  

For local development, use `./sw.sh local` instead of `./sw.sh`


> **NOTE** : The container name can be found in the `docker-compose.yml` file

> **NOTE** : The `sw.sh` script is a wrapper around the `docker-compose` command. You can use `docker-compose` instead of `./sw.sh` if you want to.



<br>

## Developer

<table>
	<tr align="center">
		<td>
		Dhruv Shah
		<p align="center">
			<img src = "https://avatars.githubusercontent.com/u/88224695" width="150" height="150" alt="Dhruv Shah">
		</p>
			<p align="center">
				<a href = "https://github.com/Dhruv9449">
					<img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36" alt="GitHub"/>
				</a>
				<a href = "https://www.linkedin.com/in/Dhruv9449" target="_blank">
					<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36" alt="LinkedIn"/>
				</a>
			</p>
		</td>
	</tr>
</table>

<p align="center">
	Made with ❤ by <a href="https://dscvit.com">GDSC-VIT</a>
</p>
