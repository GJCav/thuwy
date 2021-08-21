<template>
  <v-col class="text-center" cols="6" offset-md="3">
    <v-row class="justify-center">
      <v-img :src="require('@/assets/wy_blue.png')" max-width="384px" />
    </v-row>
    <h1>微未央（管理端）</h1>
    <v-card color="blue lighten-5" class="rounded-xl" elevation="12">
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title class="text-h5">未登录</v-list-item-title>
          <v-list-item-subtitle>请点击右上角登录</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: 'Home',
};
</script>
