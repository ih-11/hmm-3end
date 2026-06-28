# hmm-3end
A minimal demo project for exploring 3′-end / APA sequence signals using HMM

## Environment Setup

### 1. Create the Conda environment

From a terminal, navigate to the project directory and create the environment:

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

Replace `<ENV_NAME>` with the name of the environment defined in `environment.yml`:

```bash
conda activate <ENV_NAME>
```

---

### 3. Register the environment

Still inside the activated environment, run:

```bash
python -m ipykernel install \
    --user \
    --name <ENV_NAME> \
    --display-name "<ENV_NAME>"
```

This only needs to be done **once** for each Conda environment.

### 4. Open VS Code

Open the project:

```bash
code .
```

Open any notebook (`.ipynb`), click **Select Kernel**, and choose **<ENV_NAME>**.

To verify that the notebook is using the correct environment, run:

```python
import sys
print(sys.executable)
```

The output should point to the Python executable inside the Conda environment.