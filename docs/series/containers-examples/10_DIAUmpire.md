In this example I am going to demonstrate the importance of Docker through the use of a complex and powerful pipeline called DIA-Umpire. In this example I will demonstrate how to download, run and obtain the results from the DIA-Umpire pipeline.

## What do we have

The DIA-Umpire container has the following programs installed:

* DIA-Umpire v1.4256

* TPP v4.8.0

* Comet v2015010

## What do you need

Before start, you will need Docker installed on your computer. There are several ways to run Docker, go to the official [website](https://docs.docker.com/installation/) and follow the instructions on how to install it.
In order to make this analysis you will need:

* converted raw files.
* a fasta file for the database search.
* parameter files for the pipeline (see below)

## Getting the container

The first step is to download the DIA-Umpire image that is available in the BioDocker repositories:

`$ docker pull biodckr/dia-umpire`

This command will download the container to your machine. Now we need to set up a folder to be our work space, and inside this folder, create another folder called `input`:

`$ mkdir /workspace/`

`$ mkdir /workspace/input/`

The workspace folder will be where we are going to execute all commands from now on.

## Getting the parameter files

To run the pipeline we need some parameter files from the different program we will run. Go to the [DIA-Umpire repository](https://github.com/BioDocker/containers/tree/master/DIA-Umpire/1.4256/input), download all 4 files there, and place them inside the `input` folder.

### a note about sharing folders with containers

During the steps below we are going to use a specific docker parameter that allows us to map folders from our computer inside the containers. That way, the software inside the containers can have access to files in this specific folder and vice-versa. This is how we pass parameter files and retrieve results. Check [here](https://github.com/BioDocker/biodocker/wiki/Using-input--and-Output-files) for a more detailed explanation.

## 1) Run DIA-Umpire Signal Extraction

* Open the diaumpire.se_params parameter file and set the values you need.

* Define how much memory you will allow DIA-Umpire to use by setting the `-Xmx8G` parameter (see below). In this example I'm giving 8Gb to the program execution.

The analysis starts by running the DIA-Umpire program with our converted raw file, the command can look scary at first because it looks big, but this is because we are mapping folders inside the container, check the command below and then lets take a look at it in detail:

`$ docker run -v /home/felipevl/workspace/input:/data/ biodckr/dia-umpire java -jar -Xmx8G /home/biodocker/bin/DIA-Umpire/DIA_Umpire_SE.jar /data/sample.mzXML /data/diaumpire.se_params`

### explaining the command

`docker run`: is the command to execute the docker program`.

`-v /home/felipevl/workspace/input:/data/`: this docker parameter is telling to the container that we have a folder called `input/` that must be mapped inside, into a folder called `/data/`. That way, inside the container, a folder called `/data/` will be created automatically and it will share file with our folder called `input`/.

Have in mind that the container do not see the folder `/home/felipevl/workspace/input`, that's how we see the files, inside the container they will be at `/data/`.

`biodckr/dia-umpire java -jar -Xmx8G DIA_Umpire_SE.jar /data/sample.mzXML /data/diaumpire.se_params`: this last part tells that we want to execute our biodckr/dia-umpire container and, inside the container, we want to run the those commands to execute our program.

If everything goes OK you should see several new files in the input folder and the `Job complete` message in your terminal.


## 2) Converting mgf files to mzXML

The Analysis will generate several files, between them the ones we need to continue with the pipeline, that is, the `.mgf` files. The fist step create 3 new files:

* `sample_Q1.mgf`

* `sample_Q2.mgf`

* `sample_Q3.mgf`

Now we need to convert those files to a format compatible with Comet:

`$ docker run -v /home/felipevl/workspace/input:/data/ biodckr/dia-umpire /usr/local/tpp/bin/msconvert --mzXML /data/*.mgf -o /data/`

this command uses a program called msconvert, from the ProteoWizard library, present in the TPP installation. This will create a new .mzXML file for each .mgf file we have. Don't forget to always use the internal path `/data/` to save the files to the correct place.

## 3) Run a Database Search with Comet

Having all the files in the correct format we can now run the database search using Comet. Don't forget to adjust the _comet.params_ file with the desired values.

`$ docker run -v /home/felipevl/workspace/input:/data/ biodckr/dia-umpire comet.2015010.linux.exe -P/data/comet.params /data/sample_Q1.mzXML /data/sample_Q2.mzXML /data/sample_Q3.mzXML`


## 4) Run PeptideProphet and ProteinProphet from TPP Xinteract on Comet Results

Comet analysis will result in a _pep.xml_ file for each `mzXML` we have. In these case we ave now:

* `sample_Q1.pep.xml`

* `sample_Q2.pep.xml`

* `sample_Q3.pep.xml`

Now we have to run the TPP program called PeptideProphet `xinteract` with  in order to combine theses results.

In the next step when we run `ProteinProphet`, the program is expecting to see files beginning with _interact-_, so in these case we are naming our results using this prefix. Note that the parameters defined here for `xinteract` and `PeptideProphet` were selected because of the files I have and how the analysis was done. You will have to check the program documentation to set the appropriate parameters for your files.

Also note that we have to run this command individually for each _pep.xml_ file.

`$ docker run -v /home/felipevl/workspace/input:/data/ biodckr/dia-umpire /usr/local/tpp/bin/xinteract -OpdEAP -PPM -drev -N/data/interact-sample_Q1.pep.xml /data/sample_Q1.pep.xml`

ProteinProphet also is called from the `xinteract` command (check the `p` parameter).

After running the above command, you should see a message like this:

`QUIT - the job is incomplete`

You can actually ignore this. What happens here is that TPP analysis looks for a cgi script inside the web interface installation folder and one dependency may not be installed. The error appears after the PeptideProfet and ProteinProphet ends the processing.

Take a look at the `input/` folder, you will see that now we have some new _.pep.xml_ and _.prot.xml_ files too.


## 5) Run DIA-Umpire Quantification Analysis

finally, the last part!

We need now to run DIA-Umpire again, but this time using the quantification module. Before running, check the diaumpire.quant_params file, and set the correct values for you.

`$ docker run -v /home/felipevl/workspace/input:/data/ biodckr/dia-umpire java -jar -Xmx8G /home/biodocker/bin/DIA-Umpire/DIA_Umpire_Quant.jar /data/diaumpire.quant_params`

The analysis will end with a message like this:

`Job done`

And you will notice that now you have 3 more files called PeptideSummary and ProtSummary in .xls format. These are the final results from the pipeline.

## Final Remarks

This example shows how powerful docker can be. We downloaded a fully designed pipeline with all the necessary files and settings ready to use. This will allow people with difficulties in dealing with infrastructure and software configuration to go directly to the analysis step.
