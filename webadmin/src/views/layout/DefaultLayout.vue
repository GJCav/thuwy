<template>
  <div>
    <tool-bar></tool-bar>
    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
    <!-- <v-footer> </v-footer> -->
  </div>
</template>

<script>
import ToolBar from '@/components/ToolBar.vue';

export default {
  components: {
    ToolBar,
  },
};
</script>