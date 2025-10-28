from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

#LOOK INTO

# Sample Course Data
courses_data = {
    'title': ['Intro to Python', 'Advanced Python', 'Machine Learning Basics', 'Deep Learning', 'Web Development with Flask'],
    'description': [
        'Learn the fundamentals of Python programming.',
        'Explore advanced Python concepts and libraries.',
        'Introduction to machine learning algorithms and concepts.',
        'Dive into neural networks and deep learning architectures.',
        'Build web applications using Python and Flask.'
    ],
    'topics': ['programming', 'python', 'beginners', 'data science'],
    'topics': ['python', 'advanced', 'data science', 'software development'],
    'topics': ['machine learning', 'data science', 'algorithms'],
    'topics': ['deep learning', 'neural networks', 'artificial intelligence'],
    'topics': ['web development', 'python', 'flask', 'backend']
}
courses_df = pd.DataFrame(courses_data)

# Create TF-IDF vectors for course descriptions
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
course_tfidf_matrix = tfidf_vectorizer.fit_transform(courses_df['description'])

# Example User Profile (e.g., based on a course the user liked)
# Let's say the user liked 'Machine Learning Basics'
user_liked_course_index = 2
user_profile = course_tfidf_matrix[user_liked_course_index]

# Calculate cosine similarity between user profile and all courses
similarities = cosine_similarity(user_profile, course_tfidf_matrix).flatten()

# Get indices of top similar courses (excluding the liked course itself)
recommended_indices = similarities.argsort()[-4:-1][::-1] # Top 3 recommendations

# Get recommended course titles
recommended_courses = courses_df.iloc[recommended_indices]['title'].tolist()

print("Recommended Courses:", recommended_courses)