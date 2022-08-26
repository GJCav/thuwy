<template>
  <v-main>
    <v-container>
      <v-col lg="6" offset-lg="3" cols="12" offset="0">
        <!-- 展示个人基本信息 -->
        <v-row justify="center">
          <v-col cols="12" md="6">
            <h1>个人信息页</h1>
            <v-form v-if="user !== null" class="mt-5">
              <v-text-field
                v-model="user.name"
                outlined
                label="用户名"
                disabled
              ></v-text-field>
              <v-text-field
                v-model="user.clazz"
                outlined
                disabled
                label="班级"
              ></v-text-field>
              <v-text-field
                v-model="user.email"
                outlined
                disabled
                label="邮箱"
              ></v-text-field>
              <v-text-field
                v-model="user['school-id']"
                outlined
                label="学号"
                disabled
              ></v-text-field>
              <v-label>权限</v-label>
              <v-chip-group>
                <v-chip
                  :color="randColor()"
                  v-for="(privilege, key) in privileges"
                  :key="key"
                >
                  {{ privilege }}
                </v-chip>
              </v-chip-group>
            </v-form>
            <!-- 一些修改操作 -->
            <h3 v-if="user">你已经完成绑定，如需换绑请联系管理员</h3>
          </v-col>
        </v-row>
      </v-col>
    </v-container>
  </v-main>
</template>

<script>
export default {
  name: 'Profile',
  computed: {
    user() {
      return this.$store.state.user;
    },
    privileges() {
      return this.$store.state.userPrivileges;
    },
  },
  methods: {
    randColor() {
      var r = Math.floor(Math.random() * 64) + 192;
      var g = Math.floor(Math.random() * 64) + 192;
      var b = Math.floor(Math.random() * 64) + 192;
      return `#${r.toString(16)}${g.toString(16)}${b.toString(16)}`
    }
  }
};
</script>
