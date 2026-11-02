<script setup>
import { ref } from 'vue'
import BottomNav from './components/BottomNav.vue'
import HomePage from './components/HomePage.vue'
import CreateLobby from './components/CreateLobby.vue'
import LobbyWorkspace from './components/LobbyWorkspace.vue'
import ProfilePage from './components/ProfilePage.vue'
import GenerationResult from './components/GenerationResult.vue'


const activeTab = ref('home')
const lobby = ref(null)
const showResult = ref(false)

function createLobby(data) {
  lobby.value = data
  showResult.value = false
}

const titles = {
  home: 'Главная',
  catalog: 'Каталог',
  lobbies: 'Лобби',
  profile: 'Профиль',
}
</script>

<template>
  <main :class="{ 'create-page': activeTab === 'lobbies' && (!lobby || showResult), 'profile-main': activeTab === 'profile' }">
    <HomePage v-if="activeTab === 'home'" />
    <GenerationResult v-else-if="activeTab === 'lobbies' && showResult" @back="showResult = false" />
    <LobbyWorkspace v-else-if="activeTab === 'lobbies' && lobby" :name="lobby.name" @back="activeTab = 'home'" @generate="showResult = true" />
    <CreateLobby v-else-if="activeTab === 'lobbies'" @back="activeTab = 'home'" @create="createLobby" />
    <ProfilePage v-else-if="activeTab === 'profile'" />
    <h1 v-else>{{ titles[activeTab] }}</h1>
  </main>

  <BottomNav
    v-if="activeTab !== 'lobbies' || (lobby && !showResult)"
    :active-tab="activeTab"
    @change="activeTab = $event"
  />
</template>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

button,
input {
  font: inherit;
}

main {
  padding: 20px 16px 90px;
}

main.create-page {
  padding: 20px 16px;
}

main.profile-main {
  padding: 0 0 80px;
}
</style>
