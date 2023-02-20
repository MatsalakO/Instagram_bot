from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
from math import ceil
import requests
import os


class InstagramBot():

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.browser = webdriver.Chrome('C:\\lessons\\Instagram_bot\\chromedriver\\chromedriver')

	def close_browser(self):	
		'''Метод для закриття браузер '''

		self.browser.close()
		self.browser.quit()

	def login(self):
		'''Метод для логінення'''

		browser = self.browser
		browser.get('https://www.instagram.com')

		time.sleep(random.randrange(3, 5))

		username_input = browser.find_element(By.NAME, 'username')
		username_input.clear()
		username_input.send_keys(username)

		time.sleep(3)

		password_input = browser.find_element(By.NAME, 'password')
		password_input.clear()
		password_input.send_keys(password)

		password_input.send_keys(Keys.ENTER)
		time.sleep(3)

	def like_photo_by_hashtag(self, hashtag):
		'''Метод ставить лайки по хештегу'''

		browser = self.browser
		browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
		time.sleep(random.randrange(3, 5))

		for i in range(1, 4):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(random.randrange(3, 5))

		hrefs = browser.find_elements(By.TAG_NAME, 'a')
		posts_urls = []
		for item in hrefs:
			href = item.get_attribute('href')

			if "/p/" in href:
				posts_urls.append(href)

		for url in posts_urls:
			try:
				browser.get(url)
				time.sleep(3)
				like_button = browser.find_element(By.CSS_SELECTOR, 'section:first-child span button').click()
				time.sleep(random.randrange(80, 100))
			except Exception as ex:
				print(ex)
				self.close_browser()

	def xpath_exists(self, url):
		'''Метод перевіряє по xpath чи є елемент на сторінці'''

		browser = self.browser
		try:
			browser.find_element(By.XPATH, url)
			exist = True
		except NoSuchElementException:
			exist = False
		return exist

	def put_exactly_like(self, userpost):
		'''Метод ставить лайк на пост по прямій силці'''

		browser = self.browser
		browser.get(userpost)
		time.sleep(70)

		wrong_userpage = "/html/body/div[1]/section/main/div/h2"
		if self.xpath_exists(wrong_userpage):
			print('Такого поста не знайдено, перевірте URL')
			self.close_browser()
		else:
			print('Пост успішно знайдено, ставимо лайк!')
			time.sleep(2)
			like_button = 'section:first-child span button'
			browser.find_element(By.CSS_SELECTOR, like_button).click()
			time.sleep(2)

			print(f'Лайк на пост: {userpost} поставлений!')
			self.close_browser()


	def get_all_posts_urls(self, userpage):
		'''Метод збирає силки на всі пости користувача'''

		browser = self.browser
		browser.get(userpage)
		time.sleep(2)
		wrong_userpage = "/html/body/div[1]/section/main/div/h2"
		if self.xpath_exists(wrong_userpage):
			print('Користувача не знайдено, перевірте URL')
			self.close_browser()
		else:
			print('Користувача успішно знайдено, ставимо лайки!')
			time.sleep(7)	

			posts_count = browser.find_element(By.CLASS_NAME, "_ac2a").text
			posts_count = int(posts_count.replace(' ', ''))
			print(posts_count)
			loops_count = ceil(posts_count/12)

			posts_urls = []
			for i in range(0, loops_count):
				hrefs = browser.find_elements(By.TAG_NAME, 'a')
				hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

				for href in hrefs:
					posts_urls.append(href)

				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(random.randrange(2, 4))
				print(f"Ітерація #{i}")

			file_name = userpage.split("/")[-2]
			# with open(f'{file_name}.txt', 'a') as file:
			# 	for post_url in posts_urls:
			# 		file.write(post_url + "\n")

			set_posts_urls = set(posts_urls)
			set_posts_urls = list(set_posts_urls)

			with open(f'{file_name}_set.txt', 'a') as file:
				for post_url in set_posts_urls:
					file.write(post_url + '\n')


	def put_many_likes(self, userpage):
		'''Метод ставить лайки по силці на користувача'''

		browser = self.browser
		self.get_all_posts_urls(userpage)
		file_name = userpage.split("/")[-2]
		time.sleep(4)
		browser.get(userpage)
		time.sleep(4)


		with open(f'{file_name}_set.txt') as file:
			urls_list = file.readlines()
			
			for post_url in urls_list[0:6]:
				try:
					browser.get(post_url)
					time.sleep(2)
					like_button = 'section:first-child span button'
					browser.find_element(By.CSS_SELECTOR, like_button).click()
					time.sleep(random.randrange(10))
					
					print(f"Лайк на пост: {post_url}  успішно поставлений!")
				except Exception as ex:
					print(ex)
					self.close_browser()

		self.close_browser()



	def download_userpage_content(self, userpage):
		'''Метод скачує контент зі сторінки користувача'''

		browser = self.browser
		self.get_all_posts_urls(userpage)
		file_name = userpage.split("/")[-2]
		time.sleep(4)
		browser.get(userpage)
		time.sleep(4)

		# создаём папку с именем пользователя для чистоты проекта
		if os.path.exists(f"{file_name}"):
			print("Папка уже существует!")
		else:
			os.mkdir(file_name)

		img_and_video_src_urls = []
		with open(f'{file_name}_set.txt') as file:
			urls_list = file.readlines()

			for post_url in urls_list:
				try:
					browser.get(post_url)
					time.sleep(4)

					img_src = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/section/div/div[3]/div/div/div[1]/div/article[4]/div/div[2]/div/div/div/div[1]/img"
					video_src = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/section/div/div[3]/div/div/div[1]/div/article[4]/div/div[2]/div/div/div/div[1]/div/div/video"
					post_id = post_url.split("/")[-2]

					if self.xpath_exists(img_src):
						img_src_url = browser.find_element(By.XPATH, img_src).get_attribute("src")
						img_and_video_src_urls.append(img_src_url)

						# сохраняем изображение
						get_img = requests.get(img_src_url)
						with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
							img_file.write(get_img.content)

					elif self.xpath_exists(video_src):
						video_src_url = browser.find_element(By.XPATH,video_src).get_attribute("src")
						img_and_video_src_urls.append(video_src_url)

						# сохраняем видео
						get_video = requests.get(video_src_url, stream=True)
						with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
							for chunk in get_video.iter_content(chunk_size=1024 * 1024):
								if chunk:
									video_file.write(chunk)
					else:
						# print("Упс! Что-то пошло не так!")
						img_and_video_src_urls.append(f"{post_url}, немає силки!")
					print(f"Контент із поста {post_url} успішно скачаний!")

				except Exception as ex:
					print(ex)
					self.close_browser()

			self.close_browser()

		with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
			for i in img_and_video_src_urls:
				file.write(i + "\n")

my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.download_userpage_content("account")

