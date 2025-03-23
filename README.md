# CVMFS Report

By Jason Wu

## Summary

### Setup

Installing and setting up CVMFS was tedious and took several hours, the server being in WSL and the client being on macbook complicated the process.

### Onnx Inference

I uploaded the onnx model file for Microsoft's Phi-4 mini LLM to my repository and generated a response to the prompt, "Please explain how CVMFS works". The model started repeating itself for some reason, and the token generation was very slow because I ran it on cpu. The 5gb model file loaded about 0.1s slower using CVMFS compared to loading from my downloads folder. I was unsure how to measure latency in general.

## Questions

How exactly does `onnxruntime_genai` load the model file? Does the model get cached in memory/disk, or do weights get sent through http? Is there latency during token generation when using CVMFS?

I used `repo.jasonwu.org` as my repository name. from my understanding `repo` is the shorthand name for the repository while `jasonwu.org` is the domain, ie the organization that created it. Why is it set up like a DNS name and how does this format help? I noticed on the client side, the keys are stored like `.../keys/domain/name.domain.keytype`.

I also wonder if I missed a way to modify the config files from my macbook (client installation) without using `sudo chown ...`.

# Comparing Model File Formats

## LLM Output

My prompt: 
compare different ml model file formats like onnyx

Response: 
There are several different file formats for storing and deploying machine learning models, each with its own advantages and use cases. Here's a comparison of some of the most commonly used ones, including ONNX:

| Format | Full Name | Supported Frameworks | Advantages | Disadvantages |
|--------|----------|----------------------|------------|---------------|
| **ONNX** | Open Neural Network Exchange | PyTorch, TensorFlow, Keras, Scikit-learn, etc. | - Interoperability across multiple frameworks <br> - Optimized for inference <br> - Supported by ONNX Runtime for efficient execution | - Limited support for some advanced operations in certain frameworks |
| **SavedModel (TensorFlow)** | TensorFlow SavedModel | TensorFlow | - Full TensorFlow graph with metadata <br> - Supports training & inference <br> - Optimized for TF Serving & TF Lite | - Large file size <br> - Not natively compatible with other frameworks |
| **HDF5 (.h5, Keras format)** | Hierarchical Data Format | Keras, TensorFlow | - Lightweight storage format <br> - Supports both model architecture & weights <br> - Can be easily converted to other formats | - Not optimized for inference <br> - Primarily Keras-specific |
| **TorchScript (.pt, .pth)** | PyTorch Script Format | PyTorch | - Optimized for deployment <br> - Works with PyTorch JIT compilation <br> - Supports both tracing and scripting | - Less portable across frameworks |
| **PMML** | Predictive Model Markup Language | Scikit-learn, XGBoost, KNIME, R | - XML-based format for ML models <br> - Standardized for business applications <br> - Good for rule-based models | - Less common in deep learning <br> - Limited framework support |
| **CoreML (.mlmodel)** | Apple CoreML Model Format | TensorFlow, Keras, ONNX, Scikit-learn | - Optimized for iOS/macOS devices <br> - Efficient on Apple hardware <br> - Supports quantization | - Apple-specific, not portable |
| **TFLite (.tflite)** | TensorFlow Lite Model Format | TensorFlow | - Optimized for mobile & edge devices <br> - Supports quantization & reduced model size | - TensorFlow-specific <br> - Limited flexibility for training |
| **XGBoost Binary Model (.json, .bst)** | XGBoost Model Format | XGBoost | - Optimized for tree-based models <br> - Efficient for deployment | - XGBoost-specific, lacks deep learning support |

### **Which Format Should You Use?**
- If **interoperability** is important: **ONNX**  
- If using **TensorFlow** exclusively: **SavedModel** or **TFLite** for mobile  
- If using **PyTorch**: **TorchScript (.pt)**  
- If deploying on **Apple devices**: **CoreML**  
- If working with **business applications**: **PMML**  
- If working with **XGBoost**: **XGBoost’s binary model format**  

Would you like more details on converting between these formats?

## Sidenote

I wanted to know more about how Onnx enables portability. According to this [DigitalOcean article](https://www.digitalocean.com/community/tutorials/what-every-ml-ai-developer-should-know-about-onnx#onnx-in-practice) Onnx can act as a middleman format when using different ML frameworks or deploying to different platforms. For example, you could train a model using Pytorch, save it to as .onnx, then convert that to CoreML to deploy to iOS. However, is Onnx truly a standard? Based on a few community reddit threads like [this](https://www.reddit.com/r/LocalLLaMA/comments/1h54n1u/why_didnt_onnx_succeed_in_the_llm_world/) it seems opinions are mixed, Onnx can be slow or buggy and some prefer to just work with Pytorch's pt format.

# CVMFS Demo

## Stratum 0 Setup

### Background

I followed the documented [tutorial](https://cvmfs-contrib.github.io/cvmfs-tutorial-2021/02_stratum0_client/), but first I skimmed the introduction article directly preceding the tutorial. 

The goal of CernVM-FS is to distribute software (not packages/libraries!) all around the world, and it is optimized for this. It is read-only, communicates with outgoing HTTP, content-addressable, and follows POSIX specifications.

The network consists of 
- **Stratum 0**
	- A **repository** is an instance of a CVMFS file system
	- A repo is hosted on one central Stratum 0 server
	- Multiple repos can be hosted on the same Stratum 0 server
- **Stratum 1**
	- A replica server that provides a read-only mirror of a repo from Stratum 0
	- Point is for reliability, can distribute load across multiple Stratum 1 mirrors and be fault-tolerant if one mirror fails
	- Recommended to only allow clients to access Stratum 1
- **Clients**
	- Any system that mounts the `\cvmfs` filesystem
		- Data only downloaded when accessed
	- Could be personal laptops or HPC clusters

### Failed Mac Server Installation 

I followed the [documentation](https://cvmfs.readthedocs.io/en/stable/cpt-quickstart.html#getting-the-software) to install. I attempted to install using the docker image, but the image's platform was amd64 so I went for a native Fuse-t install instead using Homebrew.

After installing on homebrew using

```
brew tap macos-fuse-t/cask
brew tap cvmfs/homebrew-cvmfs
brew install cvmfs
```

I attempted to manually mount the config repo using

```
sudo mkdir -p /cvmfs/cvmfs-config.cern.ch
sudo mount -t cvmfs cvmfs-config.cern.ch /cvmfs/cvmfs-config.cern.ch
```

It failed the first time, but after restarting my macbook it worked. Maybe fuse-t needs a restart to work? I then unmounted because it did not seem necessary for the main tutorial. Now, I believe the client is successfully installed.

The main tutorial said to install 

```
sudo yum install -y epel-release # not needed on CentOS 8 sudo yum install -y https://ecsft.cern.ch/dist/cvmfs/cvmfs-release/cvmfs-release-latest.noarch.rpm sudo yum install -y cvmfs cvmfs-server
```

I have cvmfs installed through brew but brew doesn't have cvmfs-server and the website doesn't have it either so I went to use WSL Ubuntu on my pc.

### PC Server Installation

On wsl ubuntu, I followed the same stratum 0 tutorial and did

```
wget https://cvmrepo.s3.cern.ch/cvmrepo/apt/cvmfs-release-latest_all.deb
sudo dpkg -i cvmfs-release-latest_all.deb
rm -f cvmfs-release-latest_all.deb
sudo apt-get -y update
sudo apt-get -y install cvmfs cvmfs-server
```

To install the server and client package. The next step is starting up the apache http server. The docs said to use `httpd`, but I am on ubuntu so I followed the [apache docs](https://httpd.apache.org/docs/2.4/install.html) and used this command instead.

```
sudo service apache2 start
```

I then created a repository named `jasonwu.org` using 

```
sudo cvmfs_server mkfs -o $USER repo.jasonwu.org
```

And checked the keys were created using `ls /etc/cvmfs/keys`. I got a warning `Warning: Failed to restart apache after enabling necessary modules` while creating the repo, but I ran `sudo service apache2 status` to check the status and it seemed to be running fine.

I called `cvmfs_server transaction` to start a write transaction to the repo, followed the tutorial to create a simple bash file in the repo, and successfully called `cvmfs_server publish`. I decided to skip automatically resigning the whitelist using cronjob.

### Testing Client Installation

Fortunately, I can use the cvmfs installation on my mac to test a manual client installation of my repo. I copied the public key file to my macbook at `/etc/cvmfs/keys/jasonwu.org/repo.jasonwu.org.pub`. The next step is creating a config file, but first I needed to configure wsl ubuntu to accept incoming traffic. As I am not familiar with Powershell, I used ChatGPT to help me. 

#### Detour: Configuring WSL to serve requests

I got the internal ip address for wsl using 

```
hostname -I
```

then ran these commands in admin powershell to enable port forwarding then allow traffic through the windows firewall

```
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=80 connectaddress=<WSL-internal-ip> connectport=80
New-NetFirewallRule -DisplayName "Allow WSL Apache 80" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 80

```

and found my pc's ip address using `ipconfig`. I then searched up `http://my-pc-ip:80` on my macbook to confirm that the port forwarding worked.

#### Back to following the tutorial

I attempted to write to `/etc/cvmfs/config.d/repo.jasonwu.org.conf`but could not, even with sudo. So I changed the owner of the file from root to me using `chown jasonwu:staff repo.jasonwu.org.conf` then added this to the file

```
CVMFS_SERVER_URL="http://<my-pc-ip>/cvmfs/@fqrn@"
CVMFS_KEYS_DIR="/etc/cvmfs/keys/jasonwu.org"
```

Fortunately I checked that I put the key in the right folder, as I discovered I had accidently put it in `/etc/cvmfs/config.d/` instead of `/etc/cvmfs/keys/jasonwu.org`. I then created a local client config file at `/etc/cvmfs/default.local` and used the same chown trick to modify it to be

```
CVMFS_HTTP_PROXY=DIRECT
CVMFS_QUOTA_LIMIT=5000
```

So that we directly connect to the stratum 0 server and limit the cache size to 5gb. Finally comes mounting and debugging. After running

```
sudo cvmfs_config setup
sudo cvmfs_config chksetup
```

I expected an output of `OK` but got nothing. So, I went to the [advanced debugging page](https://cvmfs-contrib.github.io/cvmfs-tutorial-2021/05_advanced/#debugging-issues) and called 

```
cvmfs_config showconfig repo.jasonwu.org
```

then quickly realized I had no `SERVER_URL` set because I did not save my changes to `/etc/cvmfs/config.d/repo.jasonwu.org.conf` after doing the chown trick. I ran

```
cvmfs_config probe repo.jasonwu.org
```

to check that my change worked, and it returned `OK`. I tried running `sudo cvmfs_config chksetup` again but it failed, and then I realized that `sudo cvmfs_config setup` doesn't work on mac because there is no autofs. So, I manually mounted with

```
sudo mkdir -p /cvmfs/repo.jasonwu.org
sudo mount -t cvmfs repo.jasonwu.org /cvmfs/repo.jasonwu.org
```

Lo and behold, it successfully mounted and contains the `hello.sh` file.

### Review

That took several hours to setup. I felt like it only should have taken one hour, but I kept running into issues and had to fix them, many of which were my fault. At least it all worked in the end.

## Onnx Workflow

### Server Side

All I have to do server-side is add an onnx model file to the repo using a transaction. I decided to use Microsoft's recent [Phi-4 mini](https://huggingface.co/microsoft/Phi-4-mini-instruct) LLM. I began a transaction, used `huggingface-cli` to download the 5gb model, and published.

```
cvmfs_server transaction
cd /cvmfs/repo.jasonwu.org
huggingface-cli download microsoft/Phi-4-mini-instruct-onnx --include cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4/* --local-dir .
cd ~
cvmfs_server publish
```

### Client Side

I remounted my repo on my macbook and the Phi-4 mini files successfully showed up. I downloaded the example script for Phi-4 mini provided by microsoft using

```
curl https://raw.githubusercontent.com/microsoft/onnxruntime-genai/main/examples/python/phi3-qa.py -o phi3-qa.py
```

and modified it to remove all logic related to command line arguments and test only one prompt, "Please explain how CVMFS works", rather than loop through user input. Unfortunately I decided to use the onnx cpu runtime as there is no runtime for CoreML, which meant the output took quite a while. Here is the result:

```
Input: Please explain how CVMFS works
Generator created
Running generation loop ...

Output: CVMFS, or CernVM File System, is a file system developed by the Cern Team to provide a convenient way to distribute and execute applications and data sets in a consistent and secure manner. It is primarily used in High Energy Physics experiments and is built on top of CernVM File System (CVMFS), which is a file system developed by the Cern Team to provide a convenient way to distribute and execute applications and data sets in a consistent and secure manner.

CVMFS works by providing a way to distribute data sets and applications to users and groups of users in a consistent and secure manner. It does this by providing a way to distribute data sets and applications to users and groups of users in a consistent and secure manner. CVMFS achieves this by providing a way to distribute data sets and applications to users and groups of users in a consistent and secure manner.

CVMFS uses a combination of file system and network protocols to provide a way to distribute data sets and applications to users and groups of users in a consistent and secure manner. CVMFS uses a combination of file system and network protocols to provide a way to distribute data sets and applications to users and groups of users in a consistent and secure manner.

CVMFS uses a combination of file system and network protocols to provide a way to distribute data sets and applications to users and groups of users in a consistent and secure manner. CVMFS uses a combination of file system and network protocols to provide a way to distribute data sets and applications to users and groups of users in a consistent and secure manner.

CVMFS uses a combination of file system and network protocols to provide a way to distribute data sets and applications to users and groups of users in a consistent and secure manner. CVMFS uses a combination of file system and network protocols to provide a way to distribute data sets and applications to users and groups of users in a^C  --control+c pressed, aborting generation--


Summary
Load time: 0.38s
Prompt length: 13 tokens
New tokens: 383 tokens
Time to first: 4.94s
Prompt tokens per second: 2.63 tps
New tokens per second: 0.30 tps
```

For some reason, it kept on repeating itself, at which point I stopped the token generation. I have not debugged this issue, but it seems that the load time is very quick. Of course the token generation was very slow since I ran it on cpu, but I'm not sure if there was any latency in token gen due to CVMFS. 

I also loaded the model from my downloads folder without running token generation, and it only took 0.26s to load. After repeating this a few more times, it took 0.13-0.14s to load. I did the same test for loading from CVMFS and it took 0.36s to load the first time then 0.25-0.30 seconds to load every time afterwards. There is certainly latency, although I'm not sure how it would scale to a larger model file.

### Review

Overall, the process took less than 2 hours. It went pretty smoothly, although I was not sure how I should measure access times/latency.