# MSE485-jupyter-notebooks
Jupyter Notebooks for MSE 485 Atomistic Scale Simulations.

## Open with mybinder.org 

Open any of the links below. Note that it can be slow to load and result in Network timeout or server connection issues. 

01-periodic-boundary-conditions.ipynb [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stattlab/MSE485-jupyter-notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F%2F01-periodic-boundary-conditions%2F01-periodic-boundary-conditions.ipynb)


02-molecule-definition.ipynb  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stattlab/MSE485-jupyter-notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F%2F02-molecule-definition%2F02-molecule-definition.ipynb)


03-LJ-shift-truncate-xplor.ipynb [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stattlab/MSE485-jupyter-notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F%2F03-LJ-shift-truncate-xplor%2F03-LJ-shift-truncate-xplor.ipynb)


04-pair-correlation-function.ipynb [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stattlab/MSE485-jupyter-notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F%2F04-pair-correlation-function%2F04-pair-correlation-function.ipynb)


05-velocity-autocorrelation-function.ipynb [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stattlab/MSE485-jupyter-notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F%2F05-velocity-autocorrelation-function%2F05-velocity-autocorrelation-function.ipynb)

## Open with Google Colab 

Open any of the links below, then add the following two cells at the top:

```
!pip install -q condacolab
!git clone https://github.com/stattlab/MSE485-jupyter-notebooks.git
import condacolab
condacolab.install()
```
and 
```
%%capture
!conda install scipy matplotlib numpy gsd freud fresnel hoomd
import os
os.chdir("MSE485-jupyter-notebooks/name-of-notebook-without-ipynb/")
```

01-periodic-boundary-conditions.ipynb [![COLAB](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stattlab/MSE485-jupyter-notebooks/blob/main/01-periodic-boundary-conditions/01-periodic-boundary-conditions.ipynb)

02-molecule-definition.ipynb  [![COLAB](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stattlab/MSE485-jupyter-notebooks/blob/main/02-molecule-definition/02-molecule-definition.ipynb)

03-LJ-shift-truncate-xplor.ipynb [![COLAB](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stattlab/MSE485-jupyter-notebooks/blob/main/03-LJ-shift-truncate-xplor/03-LJ-shift-truncate-xplor.ipynb)

04-pair-correlation-function.ipynb [![COLAB](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stattlab/MSE485-jupyter-notebooks/blob/main/04-pair-correlation-function/04-pair-correlation-function.ipynb)

05-velocity-autocorrelation-function.ipynb [![COLAB](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stattlab/MSE485-jupyter-notebooks/blob/main/05-velocity-autocorrelation-function/05-velocity-autocorrelation-function.ipynb)

## Download and open locally 

You can clone this repository onto your own computer and use the `environment.yml` file to create a conda environment. You will also need to install jupyter notebook (`conda install jupyter`), and then you can execute the jupyter notebooks locally with `jupyter notebook path/to/notebook.ipynb`. 
