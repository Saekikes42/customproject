<script setup>
import { House, LayoutGrid, UsersRound, UserRound } from 'lucide-vue-next'


defineProps({
  activeTab: {
    type: String,
    default: 'home',
  },
})

const emit = defineEmits(['change'])

const tabs = [
  { id: 'home', label: 'Главная', icon: House },
  { id: 'catalog', label: 'Каталог', icon: LayoutGrid },
  { id: 'lobbies', label: 'Лобби', icon: UsersRound },
  { id: 'profile', label: 'Профиль', icon: UserRound },
]
</script>

<template>
  <nav class="bottom-nav" aria-label="Основная навигация">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      class="nav-item"
      :class="{ 'nav-item--active': activeTab === tab.id }"
      :aria-current="activeTab === tab.id ? 'page' : undefined"
      @click="emit('change', tab.id)"
    >
    <component :is="tab.icon" class="nav-icon" :size="22" :stroke-width="2" aria-hidden="true" />      <span class="nav-label">{{ tab.label }}</span>
    </button>
  </nav>
</template>

<style scoped>
.bottom-nav {
  position: fixed;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 10;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: 8px 12px calc(8px + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, 0.96);
  border-top: 1px solid #ecebfa;
  box-shadow: 0 -4px 20px rgba(54, 40, 120, 0.08);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 4px 2px;
  color: #8b89a8;
  background: transparent;
  border: 0;
  font: inherit;
  cursor: pointer;
}

.nav-icon {
  font-size: 22px;
  line-height: 1;
}

.nav-label {
  font-size: 11px;
}

.nav-item--active {
  color: #7047ff;
  font-weight: 600;
}
</style>