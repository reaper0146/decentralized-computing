FROM ubuntu:18.04
RUN apt-get update
RUN apt-get -y install curl vim git sudo wget python build-essential

ENV NVM_DIR /root/.nvm
ENV NVM_VERSION v0.34.0
ENV NODE_VERSION v10.16.3
ENV NVM_DIR /usr/local/nvm
RUN mkdir $NVM_DIR
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash

ENV NODE_PATH $NVM_DIR/$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH

RUN echo "source $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default" | bash

RUN ln -sf NVM_DIR/versions/node/$NODE_VERSION/bin/node /usr/bin/nodejs
RUN ln -sf NVM_DIR/versions/node/$NODE_VERSION/bin/node /usr/bin/node
RUN ln -sf NVM_DIR/versions/node/$NODE_VERSION/bin/npm /usr/bin/npm


RUN npm i -g truffle@5.0.37

RUN npm install -g ganache-cli@6.7.0

RUN wget https://releases.parity.io/ethereum/v2.6.3/x86_64-unknown-linux-gnu/parity
RUN chmod +x parity
RUN cp parity /usr/local/bin
RUN parity --version


RUN ARCH=`uname -m` && ETHKEY_URL=`curl -sS "https://vanity-service.parity.io/parity-binaries?version=stable&format=markdown&os=linux&architecture=$ARCH" | grep ethkey | awk {'print $5'}  | cut -d"(" -f2 | cut -d")" -f1`
RUN echo $ETHKEY_URL 
RUN wget -q $ETHKEY_URL
RUN chmod +x ethkey
RUN cp ethkey /usr/local/bin

RUN wget https://dist.ipfs.io/go-ipfs/v0.4.22/go-ipfs_v0.4.22_linux-amd64.tar.gz
RUN tar xvfz go-ipfs_v0.4.22_linux-amd64.tar.gz
RUN cd go-ipfs && ./install.sh
