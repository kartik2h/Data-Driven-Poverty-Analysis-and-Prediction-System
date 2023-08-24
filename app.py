import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace this dummy function with your actual dataset loading logic
def load_datasets():
    print("Loading datasets...")
    # Assuming you have your dataset files (train_data.csv, test_data.csv, poverty_data.csv) in the same directory as app.py
    train_data = pd.read_csv('train_labels.csv')
    test_data = pd.read_csv('test_values.csv')
    poverty_data = pd.read_csv('poverty_dataset.csv')
    
    # Prepare dictionary with dataset information
    dataset_info = {
        'train': train_data.info(),
        'test': test_data.info(),
        'poverty': poverty_data.info()
    }

    # Prepare dictionary with summary statistics
    summary_statistics = {
        'poverty': poverty_data.describe().to_dict()
    }

    return dataset_info, summary_statistics

@app.route('/api/loadData')
def get_predictions():
    print("API call...")
    dataset_info, summary_statistics = load_datasets()
    return jsonify({'dataset_info': dataset_info, 'summary_statistics': summary_statistics})

def generate_histogram():
    train_data = pd.read_csv('train_labels.csv')
    plt.figure(figsize=(8, 6))
    sns.histplot(train_data['poverty_probability'], bins=30, kde=True)
    plt.title("Distribution of Poverty Probability")
    plt.xlabel("Poverty Probability")
    plt.ylabel("Count")
    
    # Save the plot as an image file (e.g., PNG)
    image_path = 'histogram.png'
    plt.savefig(image_path)
    plt.close()  # Close the plot to release resources
    
    return image_path
    
@app.route('/api/chats')
def chats():
    # Generate the histogram and get the image path
    image_path = generate_histogram()
    
    # Prepare the chat message JSON
    chat_message = {
        "sender": "Bot",
        "message_type": "image",
        "message": "Here's the histogram for the distribution of Poverty Probability:",
        "image_url": image_path  # Keep only the filename, not the entire path
    }
    
    return jsonify({"chats": [chat_message]})

# Add a new route to serve the image
@app.route('/api/hist')
def import_image():
    print('histogram image')
    root_dir = os.getcwd()
    print('Os pwd')
    return send_from_directory(os.path.join(root_dir, 'static'), 'histogram.png')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
