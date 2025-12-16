"""
Create a simple test PDF for testing the RAG system
"""
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    # Create a simple PDF
    pdf_file = "test.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    
    # Add content
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Machine Learning Basics")
    
    c.setFont("Helvetica", 12)
    y = 700
    content = [
        "",
        "What is Machine Learning?",
        "",
        "Machine learning is a subset of artificial intelligence (AI) that enables",
        "systems to learn and improve from experience without being explicitly programmed.",
        "It focuses on developing computer programs that can access data and use it",
        "to learn for themselves.",
        "",
        "Key Concepts:",
        "",
        "1. Supervised Learning",
        "   Learning from labeled training data to make predictions on new data.",
        "   Examples: spam detection, image classification.",
        "",
        "2. Unsupervised Learning",
        "   Finding hidden patterns in unlabeled data.",
        "   Examples: customer segmentation, anomaly detection.",
        "",
        "3. Reinforcement Learning",
        "   Learning through trial and error with rewards and penalties.",
        "   Examples: game AI, robotics control.",
        "",
        "4. Neural Networks",
        "   Computing systems inspired by biological neural networks.",
        "   The foundation of deep learning.",
        "",
        "Applications:",
        "",
        "- Natural Language Processing: chatbots, translation, sentiment analysis",
        "- Computer Vision: face recognition, object detection, medical imaging",
        "- Recommendation Systems: Netflix, Amazon, Spotify suggestions",
        "- Autonomous Vehicles: self-driving cars, drones",
        "- Healthcare: disease diagnosis, drug discovery, patient monitoring",
        "",
        "Benefits of Machine Learning:",
        "",
        "1. Automation of complex tasks",
        "2. Improved accuracy over time",
        "3. Handling of large datasets",
        "4. Pattern recognition in complex data",
        "5. Personalized user experiences",
        "",
        "The field continues to evolve rapidly with new techniques",
        "and applications emerging constantly.",
    ]
    
    for line in content:
        c.drawString(100, y, line)
        y -= 20
        if y < 50:  # Start new page if needed
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750
    
    c.save()
    print(f"✅ Created {pdf_file} successfully!")
    print(f"   File ready for testing PDF upload functionality")
    
except ImportError:
    print("⚠️  reportlab not installed. Creating simple text file instead...")
    
    # Fallback: create text content
    with open("test_content.txt", "w") as f:
        f.write("""Machine Learning Basics

What is Machine Learning?

Machine learning is a subset of artificial intelligence (AI) that enables
systems to learn and improve from experience without being explicitly programmed.

Key Concepts:

1. Supervised Learning - Learning from labeled data
2. Unsupervised Learning - Finding patterns in unlabeled data  
3. Reinforcement Learning - Learning through trial and error
4. Neural Networks - Foundation of deep learning

Applications: NLP, Computer Vision, Recommendations, Autonomous Vehicles

This document can be used to test text processing if PDF creation fails.
""")
    print("✅ Created test_content.txt as fallback")
    print("   Install reportlab to create actual PDFs:")
    print('   pip install reportlab')
