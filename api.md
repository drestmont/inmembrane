# Programming API

The structure of _inmembrane_ consists of 

- top-level wrapper to manage parameters
- protocol handler
- individual plugins for each external

### The main loop and data structure

The main data structure is `proteins` a dictionary where the keys are the seqid (sequence ID) of the protein, and the value is itself a dictionary of key-value pairs. 

The program first reads a FASTA file to set up the dictionary, where at first only the 'sequence' field is created. Then the protein data structure is passed to each plugin, and progressively filled with properties generated by the plugin. 

Each plugin interfaces with an external binary, whether through a local or web-based API. The fasta sequence is processed, and the output is read, parsed, and ultimately, new properties are used to fill `proteins`.

The output of the program is printed to stdout in tab delimited format. As well, the output is always written as a Comma Separated Values file. As most of the users of the _inmembrane_ are likely biologists, CSV is used as it is a standard file format that can be used in Microsoft Excel, which most biologists are familiar with. Text files are not easily handled.


### The protocol

One of the abstractions made in _inmembrane_ is to separate the main loop and the plugins so that _inmembrane_ can accommodate the two primary protocols (one for Gram+ and one for Gram--). The choice of protocol is taken from the parameters file `inmembrane.config`. The relevant protocol is stored in a python module with the same name as the protocol in the `protocols` sub-directory.

The responsiblity of the protocol is to check for the exact plugins required (not all are needed, as there are many different possibilities) and send the fasta sequences, as stored in the `proteins` dictionary, into the plugin to get the desire property from that plugin.

Once all plugins have been successfully run, the plugin analyses the results of the external programs, and generates the final sub-cellular localisation and then, the 

### Parameters - load from file/and or input default

The approach in _inmembrane_ is to collect all relevant parameters in one place. They are found in the `inmembrane.config` file that is conveniently, stored in the Python dictionary format. The dictionary is directly read in at the initialization of the program, and stored in a dictionary internally as `params`. The protocol and plugins all expect `params` as one of the key parameters in the main function.

### Plugins

External programs are organized around each plugin. The structure of plugin is straightforward: they are python modules stored in the `plugins` directory. The name of the module reflects the name of the program as stored in the `inmembrane.config`. 

There is a function in the plugin that is called `annotate`. `annotate` always takes a `params` directory as the first parameter, and `protein` as the second parameter. There may be other parameters for the web-based version. All calls to the plugins are recognized by the module name, which can be called by `eval` within Python.

An important element of every plugin is the parsing of the results of the binary - either text processing of an output file or stdout, or HTML-scraping of the web-page output. Given that Python has excellent text-processing facilities, the files are generally parsed directly in either the main `annotate` function or an auxillary reusable function. The text files are generally sequential table-like output and so a simple iteration of the output lines is in general sufficient to process the output.

As _inmembrane_ is a glue program that builds on the work of many excellent programs, _inmembrane_ takes care to make sure credit is given. As such citations for each program are considered essential parts of the plugin, and they are stored directly in the source file, and are extracted, and displayed every time the program is run.

### Logging, temorary output and debugging

A standard approach to intermediate file is taken to standardize the process of building plugins. First STDERR is used to output program information. In order to be compatible with pure text file, program output and diagnostics are always prefaced with a # character. Because STDERR is used, this makes it easy to turn on/off the DEBUG mode, which simply redirects the STDERR output.

Give that many programs will be used, often with their own meangerie of output files, `inmembrane` always creates an intermediate output directory using the basename of the input FASTA file. A copy of the FASTA file is copied into this directory, and all subsequent calculations are made in this directory. The copy of the FASTA file is always called `input.fasta` so that subsequent OS commands can be standaradized.

As the main data structure is the standard Python dictionary `proteins`, this structure can easily be printed out using the `pprint` module in Python
