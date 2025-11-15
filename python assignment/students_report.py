import json
import os
import csv
from statistics import mean


INPUT_JSON = "student.json" 
OUTPUT_CSV = "report.csv"

def load_students(json_path):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.Please provide a file and try again.")
        return None
    try:
        with open(json_path, "r",encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON: {e}")
        return None
    except Exception as e:
        print(f"Error reading {json_path}: {e}")
        return None

def compute_avarges(students):
    results = []
    for s in students:
        sid = s.get("id","")
        name = s.get("name","")
        scores = s.get("scores",[])
        # handle empty scores gracefully hence average 0.00
        try:
            avg = round(mean(scores), 2) if scores  else 0.00
        except Exception:
            #in case the scores contain non numerical values
            numeric_scores = [x for x in scores if isinstance(x,(int,float))]
            avg = round(mean(numeric_scores),2) if numeric_scores else 0.00
        results.append({"id": sid, "name":name,"average":avg})
    return results

def write_csv(sorted_results,out_path):
    try:
        with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=["id","name","average"])
            writer.writeheader()
            for row in sorted_results:
                writer.writerow(row)
        print(f"Report written to {out_path}")
    except Exception as e:
        print(f"Error writing csv: {e}")

def main():
    students = load_students(INPUT_JSON)
    if students is not None:
        results = compute_avarges(students)

        #sort by average descending 
        sorted_results = sorted(results,key=lambda x: x["average"],reverse=True)
        write_csv(sorted_results,OUTPUT_CSV)

if __name__ == "__main__":
    main()
