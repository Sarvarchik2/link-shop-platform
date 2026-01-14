<template>
  <div class="category-list">
    <div class="category-item" v-for="category in categories" :key="category.name">
      <div class="icon-circle">
        <!-- Placeholder icon -->
        <span class="icon-text">{{ category.name[0] }}</span>
      </div>
      <span class="category-name">{{ category.name }}</span>
      <span class="item-count">{{ category.count }} Items</span>
    </div>
  </div>
</template>

<script setup>
const categories = [
  { name: 'Wayfarer', count: 12 },
  { name: 'Headliner', count: 8 },
  { name: 'Skyler', count: 5 },
  { name: 'Aviator', count: 15 },
  { name: 'Clubmaster', count: 10 },
]
</script>

<style scoped>
.category-list {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding: 10px 4px;
  scrollbar-width: none; /* Firefox */
}
.category-list::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}
.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
  cursor: pointer;
}
.icon-circle {
  width: 60px;
  height: 60px;
  background: #F5F5F5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  transition: background 0.2s;
}
.category-item:hover .icon-circle {
  background: #E0E0E0;
}
.icon-text {
  font-size: 1.5rem;
  font-weight: bold;
}
.category-name {
  font-weight: 600;
  font-size: 0.9rem;
}
.item-count {
  font-size: 0.75rem;
  color: #888;
}
</style>
