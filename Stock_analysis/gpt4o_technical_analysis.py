# gpt4o_technical_analysis.py
import os
import base64
import requests
import time

# OpenAI API Key
OPENAI_API_KEY = "Your_API_KEY"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to analyze the chart with retry mechanism for rate limits
def analyze_chart(chart_path):
    base64_image = encode_image(chart_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Price Trend Analysis: Identify the overall trend in the daily timeframe (bullish, bearish, sideways). Highlight any significant trends, consolidations, or breakouts, and specify key support and resistance levels. Assess the potential for future breakout opportunities."
                        )
                    },
                    {
                        "type": "text",
                        "text": (
                            "Technical Chart Patterns: Detect key chart patterns, including Reversal patterns (e.g., Head and Shoulders, Inverse Head and Shoulders, Double Top/Bottom), Continuation patterns (e.g., Flag, Pennant, Triangles, Rectangle), and Other patterns (e.g., Rounding Bottom, Cup and Handle, Wedge, Broadening Formation). Focus on the most significant pattern and evaluate its historical reliability."
                        )
                    },
                    {
                        "type": "text",
                        "text": "Volume Analysis: Examine volume trends to identify significant spikes in buying or selling pressure. Compare recent volume spikes to price movements and ensure weekly volume is at least three times the 20-day SMA. Highlight how volume trends support the identified price action patterns."
                    },
                    {
                        "type": "text",
                        "text": (
                            "Moving Average Insights: Analyze the stock's position relative to the 200-day moving average and the relationship between short-term and long-term moving averages (e.g., Golden Cross, Death Cross). Align moving average trends with price action and volume analysis to provide comprehensive insights."
                        )
                    },
                    {
                        "type": "text",
                        "text": "RSI Filter: Only consider stocks with an RSI between 40 and 50 to identify stocks that are not overbought or oversold and have potential for upward movement."
                    },
                    {
                        "type": "text",
                        "text": (
                            "Risk-Reward and Investment Potential: Evaluate the stock's potential for a 1:2 risk-reward ratio. Provide a detailed calculation and likelihood of reaching the target price based on historical volatility and market conditions"
                        )
                    },
                    {
                        "type": "text",
                        "text": (
                            "Comprehensive Investment Recommendation: Synthesize the above analyses to offer a clear Yes or No investment recommendation. Provide reasoning that includes trend strength, pattern reliability, and volume support. Specify entry, stop loss, and target prices, and consider potential external factors (e.g., economic news, market sentiment). Avoid conditional investment advice."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 600
    }

    retry_attempts = 5
    retry_delay = 1  # seconds

    for attempt in range(retry_attempts):
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 429:
            # Rate limit error
            print(f"Rate limit error on attempt {attempt + 1}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        else:
            return response.json()
    
    # If we exhaust retries, raise an error
    raise Exception("Exceeded maximum retry attempts due to rate limit errors")

def analyze_images_in_directory(directory):
    analysis_results = []
    # Get list of files in the directory
    image_files = os.listdir(directory)
    
    # Analyze each image in the directory
    for image_file in image_files:
        if image_file.endswith(".png"):
            image_path = os.path.join(directory, image_file)
            analysis = analyze_chart(image_path)
            analysis_results.append((image_file, analysis))
            print(f"Analysis for {image_file}: {analysis}")
    return analysis_results

def filter_yes_investment_opportunities(analysis_results):
    yes_investments = []
    for image_file, analysis in analysis_results:
        for choice in analysis['choices']:
            content = choice['message']['content']
            if "Yes" in content:
                yes_investments.append((image_file, analysis))
                break
    return yes_investments

if __name__ == "__main__":
    images_directory = "../images"
    results = analyze_images_in_directory(images_directory)
    yes_investments = filter_yes_investment_opportunities(results)
    
    for image_file, analysis in yes_investments:
        print(f"\nInvestment Opportunity for {image_file}: {analysis}")
