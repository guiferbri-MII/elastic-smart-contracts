# Setup
In this guide we will install the project's software requirements and prepare the project to execute experiments using elastic smart contracts.

## Requirements
Software requirements:
- git
- cURL
- Docker
- Go
- Npm + Node
- Python
- Hyperledger binaries

### git
[Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

If you are running on MacOS execute:
```
brew install git
```

### cURL
[Download cURL](https://curl.haxx.se/download.html)

If you are running on MacOS execute:
```
brew install curl
```

### Docker
[Download Docker](https://www.docker.com/get-started/)

If you are running on MacOS execute:
```
brew install --cask docker
```
### Go
[Download Go](https://go.dev/dl/)

If you are running on MacOS execute:
```
brew install go
```

### Nvm + Node
Install nvm to manage node versions [Download nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

To execute the project is necessary to use node version v16.19.1. Once nvm is installed, or if you have installed previously, execute:
```
nvm install 16.19.1
```

If you are using a different node version managed with nvm, execute `nvm use 16.19.1` to use the version.

### Python
[Download Python 2.7](https://www.python.org/downloads/)

You can use pyenv to manage python versions [Download pyenv](https://github.com/pyenv/pyenv)

Install matplotlib in order to display experiments results in as graphics
```
python -m pip install matplotlib 
```

### Hyperledger binaries
##### Option 1
Download the Binaries and Docker images with the following command line
```
curl -sSL https://bit.ly/2ysbOFE | bash -s -- 2.4.0 1.4.9
```
##### Option 2
Or get the install script `install-fabric.sh`

```
curl -sSLO https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh && chmod +x install-fabric.sh
```

Run the script with the next options to download the Fabric binaries. Use thes options *--fabric-version* and *-ca-version* to indicate the necessary versions.

```
./install-fabric.sh --fabric-version 2.4.0 -ca-version 1.4.9 binary
```
*For more information please check https://hyperledger-fabric.readthedocs.io/en/release-2.5/install.html*

## Steps
Once you have [installed all required](#requirements) softaware:

1. Create the working directory, e.g., *ESC*
    ```
    mkdir ESC
    ```
1. Clone the repository [galibo-infraestructure](https://github.com/governify/galibo-infrastructure) into the working directory and go to *develop* branch
1. Run docker-compose using the file *docker-compose-local.yaml*
    ```
    docker-compose -f ./docker-galibo/docker-compose-local.yaml --env-file .env up -d
    ```
1. Stop registry container
1. Clone the repository [registry](https://github.com/governify/registry) into the working directory
1. Go to `registry/infrastructure.yaml` and update the URL for registry from *'http://localhost:5400'* to ***'http://host.docker.internal:5400'***
1. Install dependencies and start **registry**
    ```
    npm install
    node index.js
    ```
1. Add *oti_gc_ansX* agreement to registry. Make a POST request with the agreement information. You can use the json file *[otig_gc_ansX.json](./docs/otig_gc_ansX.json)*
    ```
    curl --location 'http://localhost:5400/api/v6/agreements/' --header 'Content-Type: application/json' --data @otig_gc_ansX.json
    ```
1. Clone the repository [elastic-smart-contracts](https://github.com/isa-group/elastic-smart-contracts) into the working directory
1. Copy the *bin* folder downloaded [previously](#hyperledger-binaries) in *elastic-smart-contracts/bin*
1. Go to `elastic-smart-contracts/infrastructure.yaml` and update the URL for registry from *'http://localhost:5400'* to ***'http://host.docker.internal:5400'***
1. Install dependencies in the root folder
    ```
    npm install
    npm install express governify-commons oas-tools@2.1.4
    ```
1. Go to *network/connection* folder and install dependencies
    ```
    npm install
    ```
1. Go to root folder and start **elastic-smart-contracts**
    ```
    node index.js
    ```
