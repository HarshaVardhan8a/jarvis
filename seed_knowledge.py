import os
import random
from jarvis_core import Jarvis

def seed_knowledge():
    print("Initializing Jarvis for seeding...")
    jarvis = Jarvis()
    
    # "More more more data"
    facts = [
        "The speed of light is approximately 299,792,458 meters per second.",
        "Python was created by Guido van Rossum and first released in 1991.",
        "The first computer programmer was Ada Lovelace.",
        "Pinecone is a vector database that makes it easy to add long-term memory to AI applications.",
        "The mitochondria is the powerhouse of the cell.",
        "A group of flamingos is called a 'flamboyance'.",
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.",
        "The shortest war in history lasted 38 minutes between Britain and Zanzibar in 1896.",
        "Octopuses have three hearts and blue blood.",
        "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion of the iron.",
        "Diligent Corporation empowers leaders with technology, insights, and analytics.",
        "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines.",
        "Machine Learning is a subset of AI that provides systems the ability to automatically learn and improve from experience.",
        "Deep Learning is a subset of machine learning based on artificial neural networks.",
        "Streamlit is an open-source Python library that makes it easy to create and share custom web apps for machine learning and data science.",
        "LangChain is a framework for developing applications powered by language models.",
        "J.A.R.V.I.S. stands for Just A Rather Very Intelligent System.",
        "The Great Wall of China is not visible from the moon with the naked eye.",
        "Bananas are berries, but strawberries are not.",
        "The total weight of ants on Earth once equaled the total weight of humans.",
        "Water makes up about 71% of the Earth's surface.",
        "The human brain contains approximately 86 billion neurons.",
        "Quantum computing uses quantum bits, or qubits, which can exist in multiple states simultaneously.",
        "Blockchain is a decentralized ledger technology.",
        "The internet was originally called ARPANET.",
        "HTML stands for HyperText Markup Language.",
        "CSS stands for Cascading Style Sheets.",
        "JavaScript is the programming language of the Web.",
        "React is a JavaScript library for building user interfaces.",
        "Vue.js is a progressive JavaScript framework.",
        "Angular is a platform for building mobile and desktop web applications.",
        "Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.",
        "Django is a high-level Python web framework.",
        "Flask is a micro web framework written in Python.",
        "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.",
        "Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.",
        "Kubernetes is an open-source container-orchestration system for automating computer application deployment, scaling, and management.",
        "AWS (Amazon Web Services) is a comprehensive, evolving cloud computing platform provided by Amazon.",
        "Azure is a cloud computing service created by Microsoft.",
        "Google Cloud Platform (GCP) is a suite of cloud computing services that runs on the same infrastructure that Google uses internally.",
        "Linux is a family of open-source Unix-like operating systems based on the Linux kernel.",
        "Git is a distributed version control system.",
        "GitHub is a provider of Internet hosting for software development and version control using Git.",
        "VS Code is a source-code editor made by Microsoft.",
        "PyCharm is an integrated development environment (IDE) used in computer programming, specifically for the Python language."
    ]

    # Create a temporary file to ingest (since our add_document needs a file)
    temp_file = "seed_data.txt"
    with open(temp_file, "w", encoding="utf-8") as f:
        for fact in facts:
            f.write(fact + "\n\n")
    
    print(f"Seeding {len(facts)} facts into the knowledge base...")
    try:
        # Ingest
        chunks = jarvis.add_document(temp_file)
        print(f"Successfully seeded {chunks} chunks of knowledge.")
    except Exception as e:
        print(f"Seeding failed: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    seed_knowledge()
