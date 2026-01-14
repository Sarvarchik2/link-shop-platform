<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="toast"
          :class="toast.type"
          @click="remove(toast.id)"
        >
          <div class="toast-icon">
            <!-- Success -->
            <svg v-if="toast.type === 'success'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <!-- Error -->
            <svg v-else-if="toast.type === 'error'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            <!-- Warning -->
            <svg v-else-if="toast.type === 'warning'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <!-- Info -->
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
          </div>
          <span class="toast-message">{{ toast.message }}</span>
          <button class="toast-close" @click.stop="remove(toast.id)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
const { toasts, remove } = useToast()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15), 0 2px 10px rgba(0, 0, 0, 0.1);
  min-width: 300px;
  max-width: 420px;
  pointer-events: auto;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 4px solid;
}

.toast:hover {
  transform: translateX(-4px);
  box-shadow: 0 12px 50px rgba(0, 0, 0, 0.2), 0 4px 12px rgba(0, 0, 0, 0.1);
}

.toast.success {
  border-color: #10B981;
  background: linear-gradient(135deg, #ECFDF5 0%, white 100%);
}

.toast.success .toast-icon {
  color: #10B981;
  background: #D1FAE5;
}

.toast.error {
  border-color: #EF4444;
  background: linear-gradient(135deg, #FEF2F2 0%, white 100%);
}

.toast.error .toast-icon {
  color: #EF4444;
  background: #FEE2E2;
}

.toast.warning {
  border-color: #F59E0B;
  background: linear-gradient(135deg, #FFFBEB 0%, white 100%);
}

.toast.warning .toast-icon {
  color: #F59E0B;
  background: #FEF3C7;
}

.toast.info {
  border-color: #3B82F6;
  background: linear-gradient(135deg, #EFF6FF 0%, white 100%);
}

.toast.info .toast-icon {
  color: #3B82F6;
  background: #DBEAFE;
}

.toast-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.toast-message {
  flex: 1;
  font-size: 0.95rem;
  font-weight: 500;
  color: #1F2937;
  line-height: 1.4;
}

.toast-close {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #9CA3AF;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  background: #F3F4F6;
  color: #374151;
}

/* Animations */
.toast-enter-active {
  animation: toast-in 0.4s cubic-bezier(0.21, 1.02, 0.73, 1);
}

.toast-leave-active {
  animation: toast-out 0.3s cubic-bezier(0.06, 0.71, 0.55, 1);
}

@keyframes toast-in {
  0% {
    opacity: 0;
    transform: translateX(100%) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

@keyframes toast-out {
  0% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateX(100%) scale(0.9);
  }
}

/* Mobile */
@media (max-width: 480px) {
  .toast-container {
    top: auto;
    bottom: 20px;
    left: 16px;
    right: 16px;
  }
  
  .toast {
    min-width: auto;
    max-width: none;
  }
  
  .toast-enter-active {
    animation: toast-in-mobile 0.4s cubic-bezier(0.21, 1.02, 0.73, 1);
  }

  .toast-leave-active {
    animation: toast-out-mobile 0.3s cubic-bezier(0.06, 0.71, 0.55, 1);
  }

  @keyframes toast-in-mobile {
    0% {
      opacity: 0;
      transform: translateY(100%) scale(0.9);
    }
    100% {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  @keyframes toast-out-mobile {
    0% {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
    100% {
      opacity: 0;
      transform: translateY(100%) scale(0.9);
    }
  }
}
</style>

