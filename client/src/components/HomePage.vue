<script setup>
import { Bell, Search, Star, Users } from 'lucide-vue-next'
import featuredImage from '../assets/featured-sky-realms.png'

import actionIcon from '../assets/category-action.png'
import adventureIcon from '../assets/category-adventure.png'
import puzzleIcon from '../assets/category-puzzle.png'
import simulatorIcon from '../assets/category-simulator.png'
import monsterImage from '../assets/game-monster-ranch.png'
import racingImage from '../assets/game-pixel-racing.png'
import towerImage from '../assets/game-tower-brawl.png'

const categories = [
  { id: 1, name: 'Экшен', image: actionIcon },
  { id: 2, name: 'Приключения', image: adventureIcon },
  { id: 3, name: 'Головоломки', image: puzzleIcon },
  { id: 4, name: 'Симуляторы', image: simulatorIcon },
]

const games = [
  { id: 1, name: 'Monster Ranch', rating: '4.6', players: '12K', image: monsterImage },
  { id: 2, name: 'Pixel Racing', rating: '4.4', players: '8.9K', image: racingImage },
  { id: 3, name: 'Tower Brawl', rating: '4.7', players: '21K', image: towerImage },
]
</script>

<template>
  <section class="home">
    <header class="topbar">
      <label class="search-field">
        <Search class="search-icon" :size="16" :stroke-width="2" aria-hidden="true" />
        <input type="search" placeholder="Поиск игр, авторов, лобби..." />
      </label>
      <button class="notification-button" aria-label="Уведомления">
        <Bell :size="20" :stroke-width="1.8" aria-hidden="true" />
      </button>
    </header>

    <section class="featured">
      <img class="featured-image" :src="featuredImage" alt="Парящий остров с замком" />
      <span class="recommend">Рекомендуем</span>
      <div class="featured-copy">
        <h1>Sky Realms</h1>
        <p>Строй. Исследуй. Взлетай.</p>
      </div>
      <button class="play-button">Играть</button>
    </section>

    <section class="categories-section">
      <header>
        <h2>Категории</h2>
        <button>Все</button>
      </header>

      <div class="categories">
        <button v-for="category in categories" :key="category.id">
          <img class="category-image" :src="category.image" :alt="category.name" />
          <span>{{ category.name }}</span>
        </button>
      </div>
    </section>

    <section class="games-section">
      <header>
        <h2>Популярные игры</h2>
        <button>Все</button>
      </header>

      <div class="games">
        <article v-for="game in games" :key="game.id">
          <img v-if="game.image" :src="game.image" :alt="game.name" />
          <div v-else class="image-placeholder"></div>
          <h3>{{ game.name }}</h3>
          <div class="game-stats">
            <span class="game-rating"><Star :size="13" fill="currentColor" />{{ game.rating }}</span>
            <span class="game-players"><Users :size="12" />{{ game.players }}</span>
          </div>
        </article>
      </div>
    </section>
  </section>
</template>

<style>.home {
  width: 100%;
  max-width: 420px;
  margin: 0 auto;
  color: #1d1e57;
}

.topbar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.search-field {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
  height: 36px;
  padding: 0 12px;
  border-radius: 20px;
  background: #f0f1f8;
  color: #77738a;
}

.search-icon {
  width: 16px;
  height: 16px;
  flex: 0 0 auto;
}

.search-field input {
  flex: 1;
  width: 100%;
  min-width: 0;
  height: auto;
  padding: 0;
  border: 0;
  outline: 0;
  background: transparent;
  font: inherit;
  font-size: 12px;
}

.notification-button {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  padding: 0;
  border: 0;
  background: transparent;
  color: #39334f;
  cursor: pointer;
}


.featured {
  position: relative;
  min-height: 204px;
  padding: 12px;
  border-radius: 13px;
  overflow: hidden;
  border: 1px solid #d8d4e2;
  background: #f2f0f7;
  color: #17143f;
}

.featured::after {
  position: absolute;
  inset: 0 10% 0 0;
  content: '';
  background: linear-gradient(90deg, rgba(22, 66, 160, 0.78), rgba(35, 108, 210, 0.16) 72%, transparent);
  pointer-events: none;
}

.featured-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 150%;
  object-fit: cover;
}

.featured > span,
.featured button {
  position: absolute;
  z-index: 1;
}

.featured .recommend {
  top: 12px;
  left: 12px;
  display: inline-block;
  padding: 5px 17px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.3px;
  
  background: linear-gradient(100deg, #ff78d7, #fa42c4);
  color: #fff;
  z-index: 2;
}

.featured-copy {
  position: absolute;
  left: 12px;
  bottom: 50px;
  z-index: 2;
  text-align: left;
}

.featured-copy h1 {
  margin: 0 0 20px;
  font-size: 45px;
  color: #fff;
}

.featured-copy p {
  margin: 0;
  font-size: 14px;
  color: #f2f6ff;
}

.featured .play-button {
  right: 12px;
  bottom: 15px;
  z-index: 2;
  padding: 10px 50px;
  border: 0;
  border-radius: 18px;
  font-size: 20px;
  background: #7047ff;
  color: #fff;
  cursor: pointer;
}

.categories-section,
.games-section {
  margin-top: 14px;
}

.categories-section > header,
.games-section > header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  
}

.categories-section h2,
.games-section h2 {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
  color: #1d1e57;
}

.categories-section > header button,
.games-section > header button {
  border: 0;
  background: transparent;
  font-size: 10px;
  cursor: pointer;
}

.categories {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}

.categories > button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  min-width: 0;
  padding: 0;
  border: 0;
  background: transparent;
  font: inherit;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
}

.category-image {
  display: block;
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 12px;
}

.categories > button > span:last-child {
  color: #29264b;
  font-size: 10px;
  font-weight: 600;
}

.image-placeholder {
  display: block;
  width: 100%;
  aspect-ratio: 1;
  border: 1px dashed #aaa4b8;
  border-radius: 12px;
  background: #f2f0f7;
}

.games {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 7px;
}

.games article {
  min-width: 0;
}

.games article > img,
.games article > .image-placeholder {
  display: block;
  width: 100%;
  height: 84px;
  border-radius: 12px;

  margin-bottom: 5px;
  object-fit: cover;
}

.games article h3 {
  margin: 0;
  overflow: hidden;
  text-align: left;
  font-size: 13px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.game-stats {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
  font-size: 9px;
  line-height: 1;
}

.game-rating,
.game-players {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  white-space: nowrap;
}

.game-rating {
  color: #f4ae16;
}

.game-players {
  color: #85839a;
}
</style>
