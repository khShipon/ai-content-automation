import os
import random
import logging
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ContentGenerator:
    def __init__(self, topics_file='topics.txt'):
        self.topics_file = topics_file
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

    def get_random_topic(self):
        try:
            with open(self.topics_file, 'r', encoding='utf-8') as f:
                topics = [line.strip() for line in f if line.strip()]
            topic = random.choice(topics)
            logging.info(f"Selected topic: {topic}")
            return topic
        except Exception as e:
            logging.error(f"Failed to load topics: {e}")
            raise

    def generate_content(self, topic):
        prompt = f"Generate a short educational content in Bangla-English mixed format about: {topic}. Example: 'আজকে আমরা শিখবো Present Simple Tense. It is used for regular actions.'"

        # List of models to try (in order of preference)
        models = [
            "google/gemini-2.5-flash-lite-preview-06-17",
            "moonshotai/kimi-k2:free",
            "meta-llama/llama-3.2-3b-instruct:free",
            "microsoft/phi-3-mini-128k-instruct:free"
        ]

        for i, model in enumerate(models):
            try:
                logging.info(f"Trying model: {model}")

                # Add delay between attempts to avoid hitting rate limits
                if i > 0:
                    delay = 2 ** i  # Exponential backoff: 2, 4, 8 seconds
                    logging.info(f"Waiting {delay} seconds before trying {model}...")
                    time.sleep(delay)

                completion = self.client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://github.com/ai-content-automation",
                        "X-Title": "AI Content Automation Agent"
                    },
                    extra_body={},
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                content = completion.choices[0].message.content.strip()
                logging.info(f"Content generated successfully using {model}.")
                return content
            except Exception as e:
                logging.warning(f"Failed with model {model}: {e}")
                if "429" in str(e) or "rate" in str(e).lower():
                    logging.info(f"Rate limited on {model}, trying next model...")
                    continue
                else:
                    # For non-rate-limit errors, try next model
                    continue

        # If all models fail, provide a fallback
        logging.error("All models failed, using fallback content")
        fallback_content = f"আজকে আমরা শিখবো {topic} সম্পর্কে। Today we will learn about {topic}. This is an important topic for English learners. আমাদের এই বিষয়ে আরো জানতে হবে।"
        return fallback_content

if __name__ == "__main__":
    generator = ContentGenerator()
    topic = generator.get_random_topic()
    content = generator.generate_content(topic)
    print(f"Generated Content:\n{content}") 