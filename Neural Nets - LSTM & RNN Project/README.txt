This project demonstrates various recurrent neural network (RNN) architectures built with PyTorch Lightning for sequence classification tasks. It includes implementations using both vanilla RNNs and Long Short-Term Memory (LSTM) networks, each tailored for either many-to-many or many-to-one prediction tasks.

Overview
The repository contains four primary implementations:

LSTM Many-to-Many (lstm-MtoM.py)		
An LSTM-based network that produces an output for every timestep in the input sequence.

LSTM Many-to-One (lstm-Mto1.py)
An LSTM-based network that outputs a single prediction based on the final timestep.

RNN Many-to-Many (rnn-MtoM.py)
A vanilla RNN-based model that predicts at every timestep.

RNN Many-to-One (rnn-Mto1.py)
A vanilla RNN-based model that predicts a single output for the entire sequence.

Each model is built on top of a custom MultiClassModule class which standardizes training, validation, and testing procedures using cross-entropy loss and accuracy metrics from TorchMetrics.

Data and Task
The models are trained on synthetic data generated using NumPy. Each sample consists of a binary sequence where:

Input: A randomly generated binary sequence.
Target: The cumulative sum of the sequence modulo 2, effectively representing a parity or binary accumulation task.
This simple yet illustrative problem highlights the capabilities of RNNs and LSTMs in handling sequential data.

Dependencies
Ensure you have the following dependencies installed:

	Python 3.x
	PyTorch
	PyTorch Lightning
	TorchMetrics
	TorchInfo
	NumPy

You can install the required packages using pip:
	pip install torch lightning torchmetrics torchinfo numpy

Running the Models
To train any of the models, simply run the corresponding script. For example, to run the LSTM many-to-many model:
	python lstm-MtoM.py

Training logs are generated using Lightning's CSVLogger and saved in the logs directory. Additionally, model summaries are printed to the console using TorchInfo.

Project Structure
├── lstm-MtoM.py       # LSTM-based many-to-many model
├── lstm-Mto1.py       # LSTM-based many-to-one model
├── rnn-MtoM.py        # RNN-based many-to-many model
└── rnn-Mto1.py        # RNN-based many-to-one model

Model Architecture Details
Each model inherits from a common MultiClassModule that handles:

Training, Validation & Testing Steps: Using cross-entropy loss and accuracy logging.
Optimization: Configured with the Adam optimizer (learning rate = 0.001).
Key components of each model:

Embedding Layer: Transforms input tokens into dense vector representations.
Recurrent Layer: Processes sequential data using either an LSTM or vanilla RNN.
Output Layer: Applies a linear transformation to produce final predictions.
For many-to-one models, the final output is derived from the last timestep of the recurrent layer, while many-to-many models output a prediction at every timestep.

Results and Logging
The training process is logged in CSV format (using CSVLogger), which records key metrics like loss and accuracy for both training and validation. These logs can be used to monitor the learning progress and evaluate model performance.