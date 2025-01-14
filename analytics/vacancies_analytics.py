import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

MAX_SALARY = 1_000_000

currency_to_rub = {
    "AZN": 58.37,
    "BYR": 29.36,
    "EUR": 103.3,
    "GEL": 35.82,
    "KGS": 1.14,
    "KZT": 0.19,
    "RUR": 1,
    "UAH": 2.37,
    "USD": 99.23,
    "UZS": 0.0076,
}

file_name = 'vacancies_2024.csv'
vacancy = ['qa', 'test', 'тест', 'quality assurance'] 
output_folder = vacancy[0]
os.makedirs(output_folder, exist_ok=True)

df = pd.read_csv(file_name, low_memory=False)
df = df.query("salary_currency in @currency_to_rub.keys()") \
    .assign(salary_currency=lambda x: x["salary_currency"].replace(currency_to_rub))
df['Средняя зарплата'] = (df.salary_from + df.salary_to) * df.salary_currency / 2
df = df.dropna(subset='Средняя зарплата')
df = df[df['Средняя зарплата'] <= MAX_SALARY]
df['Год'] = df['published_at'].str.partition('-')[0].astype(int)
df['Город'] = df['area_name']

df_this_job = df.loc[df['name'].str.contains(vacancy[0], flags=re.IGNORECASE, regex=True)]
for i in range(len(vacancy) - 1):
    df_t = df.loc[df['name'].str.contains(vacancy[i + 1], flags=re.IGNORECASE, regex=True)]
    df_this_job = pd.concat([df_this_job, df_t])

sal_vrate_city_job = df_this_job.groupby('Город').aggregate({'Средняя зарплата': "mean", 'name': 'count'}) \
    .rename(columns={'name': 'Доля вакансий'}) \
    .sort_values('Доля вакансий', ascending=False)
sal_vrate_city_job['Доля вакансий'] = (sal_vrate_city_job['Доля вакансий'] / df_this_job['salary_currency'].count()).round(4)

vacancyRate_city_job = sal_vrate_city_job.loc[sal_vrate_city_job['Доля вакансий'] > 0.01] \
    .drop(['Средняя зарплата'], axis=1)
sal_city_job = sal_vrate_city_job.loc[sal_vrate_city_job['Доля вакансий'] > 0.01] \
    .drop(['Доля вакансий'], axis=1).rename(columns={'Средняя зарплата': 'Уровень зарплат'}) \
    .sort_values('Уровень зарплат', ascending=False)

sal_year = df.groupby('Год').aggregate({'Средняя зарплата': "mean"})
sal_year['Средняя зарплата'] = sal_year['Средняя зарплата'].astype(int)
sal_count = df.groupby('Год').aggregate({'name': "count"}) \
    .rename(columns={"name": "Количество вакансий"})

sal_year_job = df_this_job.groupby('Год').aggregate({'Средняя зарплата': "mean"})
sal_year_job['Средняя зарплата'] = sal_year_job['Средняя зарплата'].astype(int)
sal_year_job = sal_year_job.rename(columns={"Средняя зарплата": f"Средняя зарплата - {vacancy[0]} "})

sal_count_job = df_this_job.groupby('Год').aggregate({'name': "count"}) \
    .rename(columns={"name": f"Количество вакансий - {vacancy[0]} "})

sal_vrate_city = df.groupby('Город').aggregate({'Средняя зарплата': "mean", 'name': 'count'}) \
    .rename(columns={'name': 'Доля вакансий'}) \
    .sort_values('Доля вакансий', ascending=False)
sal_vrate_city['Доля вакансий'] = (sal_vrate_city['Доля вакансий'] / (df['salary_currency'].count())).round(4)

vacancyRate_city = sal_vrate_city.loc[sal_vrate_city['Доля вакансий'] > 0.01] \
    .drop(['Средняя зарплата'], axis=1)

sal_vrate_city = sal_vrate_city.dropna(subset='Средняя зарплата')
sal_vrate_city['Средняя зарплата'] = sal_vrate_city['Средняя зарплата'].astype(int)

sal_city = sal_vrate_city.loc[sal_vrate_city['Доля вакансий'] > 0.01] \
    .drop(['Доля вакансий'], axis=1).rename(columns={'Средняя зарплата': 'Уровень зарплат'}) \
    .sort_values('Уровень зарплат', ascending=False)

sal_city_to_plot = sal_city.head(10)
sal_city_to_plot.reset_index(inplace=True)

vac_rate_to_plot = vacancyRate_city.head(10)
vac_rate_to_plot.reset_index(inplace=True)
vac_rate_to_plot.loc[len(vac_rate_to_plot.index)] = ['Другие',
                                                     1 - vac_rate_to_plot['Доля вакансий'].sum()]
vac_rate_to_plot.reset_index()

plt.rcParams.update({'font.size': 8})
plt.rc('legend', fontsize=8)
ax = sal_year.join(sal_year_job).plot.bar(title='Уровень зарплат по годам')
ax.figure.savefig(os.path.join(output_folder, '1.png'), dpi=300)

fig, axes = plt.subplots(nrows=2)
sal_count.join(sal_count_job).plot.bar(title='Количество вакансий по годам', ax=axes[0])
axes[0].grid(axis='y')
sal_count_job.plot.bar(title='Количество вакансий по годам', color=(1, 0.49609375, 0.0546875), ax=axes[1])
axes[1].grid(axis='y')

plt.tight_layout()
fig.savefig(os.path.join(output_folder, '2'), dpi=300)
plt.show()
fig, ax1 = plt.subplots()
ax1.barh(sal_city_to_plot['Город'][::-1], sal_city_to_plot['Уровень зарплат'][::-1], color='#FF5733')
ax1.set_title('Уровень зарплат по городам')
ax1.tick_params(axis='y', labelsize=6)
ax1.grid(axis='x')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, '4.png'), dpi=300)

fig, ax2 = plt.subplots()
colors = ['#FF5733', '#33FF57', '#5733FF', '#FF33C7', '#33C7FF', '#C7FF33', '#FF3362', '#3362FF', '#FFD700',
          '#8B4513', '#00FFFF']
ax2.pie(x=vac_rate_to_plot['Доля вакансий'], colors=colors, labels=vac_rate_to_plot['Город'],
        textprops={'fontsize': 6})
ax2.set_title('Доля вакансий по городам')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, '3.png'), dpi=300)
plt.close()

vac_rate_job_to_plot = vacancyRate_city_job.head(10)
vac_rate_job_to_plot.reset_index(inplace=True)
vac_rate_job_to_plot.loc[len(vac_rate_job_to_plot.index)] = ['Другие',
                                                             1 - vac_rate_job_to_plot['Доля вакансий'].sum()]
fig, ax3 = plt.subplots()
ax3.pie(x=vac_rate_job_to_plot['Доля вакансий'], labels=vac_rate_job_to_plot['Город'],
        autopct='%1.1f%%', textprops={'fontsize': 6}, colors=plt.cm.Paired.colors)
ax3.set_title(f'Доля вакансий по городам {vacancy[0]}')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, '5.png'), dpi=300)
plt.close()

sal_city_job_to_plot = sal_city_job.head(10)
sal_city_job_to_plot.reset_index(inplace=True)
fig, ax4 = plt.subplots()
ax4.barh(sal_city_job_to_plot['Город'][::-1], sal_city_job_to_plot['Уровень зарплат'][::-1], color='#33AFFF')
ax4.set_title(f'Уровень зарплат по городам {vacancy[0]}')
ax4.tick_params(axis='y', labelsize=6)
ax4.grid(axis='x')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, '6.png'), dpi=300)
plt.close()

##### Таблички для востребованности
text_file = open(os.path.join(output_folder, "salary_level_by_year_general.html"), "w")
text_file.write(sal_year.to_html())
text_file.close()
text_file = open(os.path.join(output_folder, "salary_level_by_year.html"), "w")
text_file.write(sal_year_job.to_html())
text_file.close()
text_file = open(os.path.join(output_folder, "num_of_vac_by_year_general.html"), "w")
text_file.write(sal_count.to_html())
text_file.close()
text_file = open(os.path.join(output_folder, "num_of_vac_by_year.html"), "w")
text_file.write(sal_count_job.to_html())
text_file.close()

##### Таблички для /geography

text_file = open(os.path.join(output_folder, "salary_level_by_city_general.html"), "w")
text_file.write(sal_city.to_html())
text_file.close()
text_file = open(os.path.join(output_folder, "dolya_of_vac_by_city_general.html"), "w")
text_file.write(vacancyRate_city.to_html())
text_file.close()

##### Таблички для /geography
text_file = open(os.path.join(output_folder, "salary_level_by_city.html"), "w")
sal_city_job['Уровень зарплат'] = sal_city_job['Уровень зарплат'].round(0).astype(int)
text_file.write(sal_city_job.to_html())
text_file.close()

text_file = open(os.path.join(output_folder, "dolya_of_vac_by_city.html"), "w")
text_file.write(vacancyRate_city_job.to_html())
text_file.close()