print("Start")
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 

df = pd.read_csv('data/data.csv')
# print(df.info())

#DATA CLEANING
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
# print(df.columns.tolist())
df= df.drop_duplicates() 

#NUMERIC COLUMNS CLEANING

df['price'] = df['price'].astype(str).str.replace(',', '').astype(float)
# print(df['price'])

df['area'] = df['area'].astype(str).str.replace(',', '').astype(int)
# print(df['area'])

df['rate_per_sqft'] = df['rate_per_sqft'].astype(str).str.replace(',', '').astype(float)
# print(df['rate_per_sqft'])

# CATEGORICAL COLUMNS CLEANING
df['status'] = df['status'].str.strip().str.lower()
df['rera_approval'] = df['rera_approval'].str.strip().str.lower().map({"approved by rera": True,"not approved by rera": False})
df['flat_type'] = df['flat_type'].str.strip().str.lower()   

df = df.drop_duplicates()

# QUESTION 1:WHICH IS THE COSTLIEST FLAT IN THE DAT SET?
costliest_flat = df.loc[df['price'].idxmax()]

print(f" the costliest flat is a {costliest_flat['bhk_count']} BHK {costliest_flat['flat_type']} located in {costliest_flat['locality']}, built by {costliest_flat['builder_name']}. It is currently {costliest_flat['status']} and has an area of {costliest_flat['area']} sqft, priced at {costliest_flat['price']/10000000:.2f} Crores. The rate per sqft is {costliest_flat['rate_per_sqft']}. RERA approval status: {'Approved' if costliest_flat['rera_approval'] else 'Not Approved'}.")

# QUESTION 2 : WHICH LOCALITY HAS THE HIGHEST AVERAGE PRICE ?
highest_avg_price_locality = df.groupby('locality')['price'].mean().idxmax()
avg_price = df.groupby('locality')['price'].mean().max()

print(f"The locality with the highest average price is {highest_avg_price_locality} and the average price in {highest_avg_price_locality} is {avg_price/10000000:.2f} Crores.")

# QUESTION 3:  WHICH LOCALITY HAS THE HIGHEST  RATE PER SQUARE FOOT ?
highest_avg_rate_locality = df.groupby('locality')['rate_per_sqft'].mean().idxmax()
avg_rate = df.groupby('locality')['rate_per_sqft'].mean().max()

print(f"The locality with the highest average rate per sqft is {highest_avg_rate_locality} and the average rate in {highest_avg_rate_locality} is {avg_rate:.2f} Rs/sqft.")


# QUESTION 4 : DO READY TO MOVE PROPERTY COST MORE THAN UNDER CONSTRUCTION PROPERTIES?
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean()
under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean()

if ready_to_move_avg_price > under_construction_avg_price:
    print(f"Yes, ready to move properties cost more than under construction properties. The average price of ready to move properties is {ready_to_move_avg_price/10000000:.2f} Crores, while the average price of under construction properties is {under_construction_avg_price/10000000:.2f} Crores.")   
else:
    print(f"No, under construction properties cost more than ready to move properties. The average price of under construction properties is {under_construction_avg_price/10000000:.2f} Crores, while the average price of ready to move properties is {ready_to_move_avg_price/10000000:.2f} Crores.")
    
    
# # QUESTION 5 : DO RERA APPROVED PROPERTIES COMMAND A PRICE PREMIUM?
rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean()
rera_not_approved_avg_price = df[df['rera_approval'] == False]['price'].mean()

if rera_approved_avg_price > rera_not_approved_avg_price:
    print(f"Yes, RERA approved properties command a price premium. The average price of RERA approved properties is {rera_approved_avg_price/10000000:.2f} Crores, while the average price of non-RERA approved properties is {rera_not_approved_avg_price/10000000:.2f} Crores.")  
    
else:
    print(f"No, non-RERA approved properties command a price premium. The average price of non-RERA approved properties is {rera_not_approved_avg_price/10000000:.2f} Crores, while the average price of RERA approved properties is {rera_approved_avg_price/10000000:.2f} Crores.")
    
    
# #QUESTION 6 : HOW DOES AREA IMPACT PRICE AND RATE PER SQUARE FOOT?
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)                
plt.scatter(df['area'], df['price'])
plt.xlabel('Area (sqft)')
plt.ylabel('Price (Crores)')
plt.title('Impact of Area on Price')    
plt.subplot(1, 2, 2)
plt.scatter(df['area'], df['rate_per_sqft'])        
plt.xlabel('Area (sqft)')       
plt.ylabel('Rate per sqft (Rs/sqft)')
plt.title('Impact of Area on Rate per sqft')
plt.tight_layout()  
plt.savefig("images/area_analysis.png", dpi=300, bbox_inches="tight")
plt.show()


#QUESTION 7 : WHICH BHK CONFIGURATION IS MOST EXPENSIVE?
most_expensive_bhk = df.groupby('bhk_count')['rate_per_sqft'].mean().idxmax()
print(f" the most expensive bhk configuration on average is {most_expensive_bhk}BHK")


# QUESTION 8 : WHICH PROPERTY TYPE IS COSTLIEST?
most_expensive_property_type = df.groupby('flat_type')['rate_per_sqft'].mean().idxmax()
print(f"the most expensive property type is {most_expensive_property_type}")



#QUESTION 9 : DO CERTAIN BUILDERS PRICE HIGHER?
builder_price = df.groupby('company_name')['rate_per_sqft'].mean().sort_values(ascending=False).head(5)
print(builder_price)

# QUESTION 10 : ARE LARGER HOMES MORE EXPESIVE PER SQFT?
sns.scatterplot(data=df, x='area', y='rate_per_sqft')

plt.title("Area vs Rate per Sqft")
plt.xlabel("Area (sqft)")
plt.ylabel("Rate per Sqft")

plt.savefig("images/area_vs_rate_per_sqft.png", dpi=300, bbox_inches="tight")

plt.show()

# QUESTION 11 :Which locality offers the best value for money?

value = df.groupby('locality')['rate_per_sqft'].mean().sort_values(ascending=False).head(10)

print(value)

#question 12 : WHICH SECTOR IS BEST FOR THE FIRST-TIME  HOME BUYER?
first_time = df.groupby('locality')['price'].mean().sort_values().head(10)

print(first_time)

#QUESTION 13 : WHICH SECTOR IS BEST FOR THE LUXURY PROPERTY INVESTMENT ? 
luxury = df.groupby('locality')['price'].mean().sort_values(ascending=False).head(10)

print(luxury)

#QUESTION 14 : WHICH BUILDER PROVIDES THE BEST VALUE FOR MONEY ?

builder_value = df.groupby('company_name')['rate_per_sqft'].mean().sort_values().head(10)

print(builder_value)

# QUESTION 15 : Which sector should an investor choose?   Create a score based on:Lower average price Higher availability  Lower rate per sqft

investment = df.groupby('locality').agg({
    'price':'mean',
    'rate_per_sqft':'mean'
})

investment = investment.sort_values(
    by=['price','rate_per_sqft'],
    ascending=True
)

print(investment.head(10))

#===========================================
# QUESTION 16 : SALARY BASED PROPERTY RECOMMENDATION SYSTEM

salary = int(input("\nEnter Your Monthly Salary (₹): "))

annual_salary = salary * 12
budget = annual_salary * 5

print("\nEstimated Affordable Property Budget : ₹", budget)

recommend = df[df['price'] <= budget]

recommend_sector = recommend.groupby('locality')['price'].mean().sort_values().head(10)

print("\nTop Recommended Localities Within Your Budget\n")
print(recommend_sector)

recommend_rate = recommend.groupby('locality')['rate_per_sqft'].mean().sort_values().head(10)

print("\nAverage Rate Per Sqft\n")
print(recommend_rate)

print("\nPurpose")
print("1. Self Living")
print("2. Investment")

choice = int(input("Enter Choice : "))

if choice == 1:
    recommend = df[df['price'] <= budget]

    result = recommend.groupby('locality')['price'].mean().sort_values().head(10)

    print("\nBest Localities For Living\n")
    print(result)

elif choice == 2:
    recommend = df[df['price'] <= budget]

    result = recommend.groupby('locality')['rate_per_sqft'].mean().sort_values(ascending=False).head(10)

    print("\nBest Localities For Investment\n")
    print(result)