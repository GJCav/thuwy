<template>
<div>
  <button @click="test">click this</button>
  <span>{{(userPrivileges)}}</span> <br>
  <span>{{groupPrivilegeInfo}}</span> <br >
  <span>{{(allPrivileges)}}</span>
</div>
</template>


<script>
import * as auth from "./../backend-api/auth"
import { mapGetters } from "vuex"

export default {
  name: "UserListView",
  data: () => ({
 
  }),

  computed: {
    ...mapGetters(["userPrivileges", "groupPrivilegeInfo", "allPrivileges"])
  },

  methods: {
    async test(){
      console.log(await auth.fetchUserList({}))
    }
  },
}
</script>