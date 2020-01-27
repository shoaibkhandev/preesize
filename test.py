from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import sent_tokenize
import requests
from bs4 import BeautifulSoup

# url = 'https://newshunt.io/english/story/221063/for-diksha-dagar-its-about-the-winning-attitude-times-of-india'
# res = requests.get(url)
# html_page = res.content
# soup = BeautifulSoup(html_page, 'html.parser')
# text = soup.find_all(text=True)

# print(text)

analyzer = SentimentIntensityAnalyzer()
# text = "The annual United Nations General Assembly (UNGA) debates in New York kick off today, with the latest Iran crisis, climate change , global development and denuclearization expected to be key issues on the agenda of many world leaders. Starting Tuesday, political leaders will take to the General Assembly’s floor to deliver speeches. The gathering remains the world’s leading and most-watched forum for leaders to gather at the United Nations headquarters to discuss global issues. This year, Russian President Vladimir Putin and Chinese President Xi Jinping will not be attending. However, 196 representatives from around the world will deliver statements. The UNGA will also be a hyperactive nerve centre for global diplomacy over the coming week: Including those that were conducted on Monday, some 560 official meetings are planned to be held and UN Secretary-General Antonio Guterres will participate in 140 bilateral meetings when it is all said and done. Key Speakers According to United Nations tradition, the leader of Brazil will be the first to speak on Tuesday morning, followed by the United States, the organisation's host country. Iranian President Hassan Rouhani and Yemen’s President Abdrabuh Mansour Hadi will speak during the week of scheduled General Assembly addresses. Hadi will address the armed conflict that has been ongoing in the country since 2015. The United Nations has repeatedly called the Yemeni conflict the world’s worst humanitarian crisis, with an estimated 24 million people - nearly 80 percent of the country’s population - currently in need of aid and protection. In June, international rights organisations put the cumulative death toll in the war as fast approaching 100,000, British media reported. The 100,000 benchmark figure has probably since been exceeded. Other keynote speakers on Tuesday at the General Assembly will be the leaders or senior ministers from France, Canada, Turkey, South Korea, and the United Kingdom. On Wednesday, the UN General Assembly debate will continue, with scheduled statements including that of the head of the Libyan Government of National Accord (GNA), Fayez Sarraj. On Thursday, Venezuelan Vice President Delcy Rodriguez and Foreign Minister Jorge Arreaza, representing the country’s government, will speak, and said they plan to address US sanctions imposed against their country. On Friday, Russia’s Foreign Minister Sergey Lavrov will deliver his speech to the world body. According to Russia’s Ambassador to the United Nations, Vassily Nebenzia, Moscow’s priorities include the promotion of multilateralism, arms control, and cybersecurity. Israeli Prime Minister Benjamin Netanyahu, as well as the representatives of China, India, Pakistan, Sudan, and The Bahamas, will also convey their messages to the world on that day. However, Netanyahu, who is seeking to remain prime minister after the Israeli elections last week, is not expected to attend this year’s UN General Assembly. On Saturday, Syrian Deputy Foreign Minister Faisal Al Mekdad may address the UN General Assembly about the creation of the Syrian Constitutional Committee. Next Monday, 30 September, on the final day of the General Debate, representatives of Saudi Arabia, Afghanistan, and North Korea - among other states - are expected to highlight the event. North Korean Foreign Minister Ri Yong Ho will skip the UN General Assembly session this year and Ambassador to the United Nations Kim Song will represent Pyongyang. The North Korean government has recently expressed readiness to resume denuclearisation talks with the United States in the second half of September, but Pyongyang has at the same time been conducting missile tests. World Leader Meetings Many world leaders will hold talks on the sidelines of the General Assembly throughout the week in both bilateral and multilateral settings to address issues ranging from the elimination of nuclear weapons and the implementation of the Agenda for Sustainable Development to the situation in Afghanistan and the prevention of an arms race in outer space. Although there have been reports about the possibility that US President Donald Trump and Iran President Hassan Rouhani will meet during the Debate Week, the counterparts will not convene for bilateral talks. On Wednesday, Trump is expected to hold a bilateral meeting with Ukrainian President Volodymyr Zelensky on the sidelines of the General Assembly to discuss Minsk obligations, China's economic activity in the country, energy cooperation, and other mutual matters, a senior US administration official told reporters on Friday. Trump is also scheduled to hold individual meetings with the leaders of Egypt, El Salvador, India, Iraq, Japan, New Zealand, Pakistan, Poland, Singapore, South Korea, and the United Kingdom, the official added. “They're going to examine further opportunities as has recently been taken on energy cooperation... they're going to talk about opportunities for further reform of Ukraine's economy, additional trade opportunities, and the president is going to speak to his concerns about what he sees as predatory Chinese economic activity in Ukraine to loot Ukraine's intellectual property,\" a White House official told reporters last week. On Wednesday, Trump will meet with Western Hemisphere leaders at the UN General Assembly to discuss Venezuela, a senior Trump administration official said during a conference call on Friday. Most of the countries of the Western Hemisphere, with the notable exceptions of Cuba, Uruguay, Nicaragua, El Salvador, and Bolivia, don't recognise the government of President Nicolas Maduro. US Secretary of State Mike Pompeo on Friday will meet with top Russian diplomat Sergei Lavrov on the sidelines of the UN General Assembly, the State Department announced Sunday. France, the United Kingdom, and Germany plan to discuss the situation around the Iranian nuclear deal at the upcoming UN General Assembly in New York, French Foreign Minister Jean-Yves Le Drian said on Sunday. Other Notable Events Pompeo will convene with members of the Gulf Cooperation Council (GCC) and Jordan during the General Assembly this week to discuss a possible response to Iran's \"escalatory violence\", a senior Trump administration official said during a conference call last Friday. Apart from the General Debate, the UN General Assembly session will, for the first time, review the progress on the implementation of the 2030 Agenda for Sustainable Development on Tuesday and Wednesday. The 17 Sustainable Development Goals, adopted in 2015, including eradicating poverty, hunger, reducing inequality, combating climate change , achieving gender equality, and promoting quality education and responsible consumption, among others. On Thursday, the UN General Assembly will convene its first High-Level Dialogue on Financing for Development since the adoption of the Addis Ababa Action Agenda. On Friday, the General Assembly will hold a one-day high-level review of the progress made in addressing the priorities of Small Island Developing States (SIDS) through the implementation of the SAMOA Pathway. The General Assembly has decided that the high-level review will result in a concise action-oriented and inter-governmentally agreed political declaration"
# sentences = sent_tokenize(text)
sentence = "VADER is not smart, handsome, nor funny"

print("Sentiment using vaderSentiment")
vspos = 0
vsneg = 0
vsneu = 0
tot = 0
# for sentence in sentences:
vs = analyzer.polarity_scores(sentence)
print(sentence,vs)
if vs['compound'] >= 0.05:
    vspos = vspos + 1
    print("Sentence is positive using vaderSentiment")
elif (vs['compound'] > -0.05 and vs['compound'] < 0.05):
    vsneu = vsneu + 1
    print("Sentence is neutral using vaderSentiment")
elif vs['compound'] <= -0.05:
    vsneg = vsneg + 1
    print("Sentence is negative using vaderSentiment")
# tot = len(sentences)
print("Positive: ",vspos," Negative: ",vsneg," Neutral: ",vsneu," Total: ")
# print("Positive: ",round((vspos/tot)*100,1)," Negative: ",round((vsneg/tot)*100,1)," Neutral: ",round((vsneu/tot)*100,1)," Total: ","100%")
# print("-----------------------------------------------------------------------------------")

print("Sentiment using TextBlob")
tbpos = 0
tbneg = 0
tbneu = 0
# for sentence in sentences:
tb = TextBlob(sentence).sentiment
print(sentence,tb)
if tb.polarity > 0:
    tbpos = tbpos + 1
    print("Sentence is positive using TextBlob")
elif tb.polarity == 0:
    tbneu = tbneu + 1
    print("Sentence is neutral using TextBlob")
elif tb.polarity < 0:
    tbneg = tbneg + 1 
    print("Sentence is negative using TextBlob")

print("Positive: ",tbpos," Negative: ",tbneg," Neutral: ",tbneu)
# print("Positive: ",round((tbpos/tot)*100,1)," Negative: ",round((tbneg/tot)*100,1)," Neutral: ",round((tbneu/tot)*100,1)," Total: ","100%")
