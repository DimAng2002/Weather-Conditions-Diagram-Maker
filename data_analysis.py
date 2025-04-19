import os
import re
from datetime import date, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def takeValues(arxeio):
    with open(arxeio, "r") as file:
        content = file.read()
        temp_pattern = r'--+\n\s+(\d+\.\d+)\s+(\d+\.\d+)'
        temp_match = re.search(temp_pattern, content)

        if temp_match:
            avg_temp = float(temp_match.group(1))
            return avg_temp 
        
        """
        lines = content.strip().split('\n')
        for line in reversed(lines):
            if line.strip() and not line.startswith('Max >=') and not line.startswith('--'):
                values = re.findall(r'(\d+\.\d+|\d+)', line)
                avg_temp = float(values[0])
        """

def create_plot_for_region(region_data, region_name):
    dates = []
    temperatures = []
    date_objects = []

    for data in region_data:
        if 'year' in data and 'month' in data and 'temperature' in data:
            month_clean = data['month'].split()[0]
            date_obj = datetime.strptime(f"{data['year']}-{month_clean}", "%Y-%m")
            temp = float(data['temperature']) if isinstance(data['temperature'], str) else data['temperature']
            date_objects.append((date_obj, temp))
    
    date_objects.sort(key=lambda x: x[0])  
    
    for date_obj, temp in date_objects:
        dates.append(date_obj)
        temperatures.append(temp)
    
    plt.figure(figsize=(20, 9))
    plt.plot(dates, temperatures, marker='o', linestyle='-')
    plt.title(f"Μέση θερμοκρασία περιοχής {region_name}")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Θερμοκρασία (°C)")
    plt.grid(True)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(os.path.join("Diagrams", f"{region_name}_temperature.png"))
    plt.close()
    print(f"Το διάγραμμα για την περιοχή {region_name} δημιουργήθηκε")

def main():
    perioxes = []
    regionData = {}
    
    for arxeio in os.listdir("Text_Files"):
        if arxeio.endswith(".TXT"):
            region = arxeio.split('-')[0]
            if region not in perioxes:
                perioxes.append(region)
                regionData[region] = []
    
    for perioxi in perioxes:
        print(f"=-=-=-=-=-=-=-=-={perioxi}-=-=-=-=-=-=-=-=-=")
        
        for arxeio in os.listdir("Text_Files"):
            if arxeio.endswith(".TXT") and arxeio.startswith(perioxi):
                parts = arxeio.split('-')
                if len(parts) >= 3:
                    year = parts[1]
                    month = parts[2].split('.')[0]
                    
                    file_path = os.path.join("Text_Files", arxeio)
                    temperature = takeValues(file_path)
                    
                    regionData[perioxi].append({'year': year,'month': month,'temperature': temperature})
                                
        if perioxi in regionData:
            create_plot_for_region(regionData[perioxi], perioxi)

if __name__ == "__main__":
    main()