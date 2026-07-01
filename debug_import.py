import sys
print("start")
sys.path.insert(0, r"C:\Users\Jatin Lakhani\Desktop\InterviewGPT")
try:
    import app
    print("imported app")
except Exception as e:
    import traceback
    traceback.print_exc()
