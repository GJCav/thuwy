<template>
  <div
    class="section-part fx"
    :style="{ marginBottom: showList ? '0px' : '34px' }"
  >
    <div class="avatar"></div>

    <div class="chat-frame">
      <div class="chat" :style="{ minHeight: height }">
        <div class="cf-head"></div>
        <div class="content-box">
          <slot></slot>
        </div>
      </div>

      <!-- 尾部列表 -->
      <div class="foo-list" v-if="showList">
        <div class="foo-item fx" v-for="item in 2" :key="item">
          <div class="min-avatar"></div>
          <div class="info"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SectionPart",
  props: {
    //是否展示尾部列表
    showList: {
      type: Boolean,
      default: false,
    },
    //自定义高
    height: {
      type: String,
      default: "287px",
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.section-part .avatar {
  width: 80px;
  height: 80px;
  background: #ebeff4;
  border-radius: 100%;
  margin-right: 17px;
}

.section-part .chat {
  width: 908px;
  min-height: 287px;
  background: #ebeff4;
  border-radius: 10px;
}

.section-part .chat .cf-head {
  width: 908px;
  height: 80px;
  background: #0077ff;
  position: relative;
}

.section-part .chat .cf-head::before {
  content: "";
  position: absolute;
  width: 0;
  height: 0px;
  top: 50%;
  left: -30px;
  transform: translateY(-50%);
  border: 17px solid transparent;
  border-color: transparent;
  border-right-color: #0077ff;
}

.section-part .chat .content-box {
  padding: 4px 21px;
  overflow: hidden;
}

.section-part .foo-list {
  width: 877px;
  height: auto;
  border-left: 1px solid #000;
  margin-left: 46px;
  padding-top: 42px;
}

.section-part .foo-list .foo-item {
  margin-left: -16px;
  padding-bottom: 42px;
}

.section-part .foo-list .foo-item .min-avatar {
  width: 32px;
  height: 32px;
  background: #ebeff4;
  border-radius: 100%;
}

.section-part .foo-list .foo-item .info {
  width: 829px;
  height: 32px;
  background: #ebeff4;
  margin-left: 16px;
}
</style>
