<template>
  <div class="about" style="text-align: center">
    <div class="cover-box">
      <img src="@/assets/cover2.png" alt="" />
      <div class="text">
        <p>Welcome</p>
        <p>To</p>
        <p>微未央's blog！</p>
      </div>

      <div class="desc">
        欢迎大家在这里留下你的问题 或者提出你的想法与建议呦
      </div>

      <!-- 提问按钮 -->
      <router-link class="btn" to="/issue/0/">我要提问</router-link>
    </div>

    <!-- <div class="d-flex flex-column"> -->
    <!-- 最新提问与回答 -->
    <a class="quie-and-reply"> 最新提问与回答 </a>
    <v-card width="800" class="mx-auto" flat>
      <v-list>
        <v-list-item
          v-for="article in articlelist"
          :key="article.id"
          class="my-10 elevation-3"
        >
          <!-- Video Image -->
          <v-list-item-avatar tile width="120" height="120">
            <v-img class="rounded-lg" src="@/assets/wy_blue.png"></v-img>
          </v-list-item-avatar>
          <!-- Video Description-->
          <v-list-item-content class="align-self-start">
            <v-list-item-title class="text-left text-h5">
              {{ article.title }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-left">
              <v-chip color="success" class="mr-2" label small> NEW </v-chip>
              <v-chip color="warning" class="mr-2" label small> HOT </v-chip>
            </v-list-item-subtitle>
            <div class="text-caption grey--text">{{ article.content }}</div>
          </v-list-item-content>
          <!-- Video Start Button-->
          <v-list-item-action>
            <v-btn
              :to="`/blog/${article.id}/`"
              color="info"
              class="rounded-pill"
              >了解更多</v-btn
            >
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-card>
    <!-- 列表 -->
    <!-- <div class="list">
        <div class="list-item fx" v-for="item in 3" :key="item">
          <div class="img"></div>
          <div class="right fxg">
            <div class="bar fx-b">
              <v-container class="d-flex">
                <div class="tag" :style="`background:${color[item - 1]}`">
                  #LABEL
                </div>
                <div class="warp fx-b">
                  <span>发布时间</span>
                  <span>回复时间</span>
                  <span>状态</span>
                </div>
              </v-container>
            </div>

            <h2>Username1</h2>
          </div>
        </div>
      </div> -->
    <!-- </div> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      color: ["#18A5CA", "#9C6CDA", "#ECC331"],
      articlelist: [
        { id: 1, title: "文章的标题", content: "文章的简要内容" },
        { id: 2, title: "文章的标题", content: "文章的简要内容" },
        { id: 3, title: "文章的标题", content: "文章的简要内容" },
        { id: 4, title: "文章的标题", content: "文章的简要内容" },
      ],
    };
  },
};
</script>



<style scoped>
.cover-box {
  position: relative;
}

.cover-box img {
  width: 100%;
  height: 880px;
}

.cover-box .text,
.cover-box .desc,
.cover-box .btn {
  text-align: start;
  position: absolute;
}

.cover-box .text {
  top: 58px;
  left: 80px;
  width: 623px;
  height: 397px;
}

.cover-box .text p {
  font-family: "Times New Roman", Times, serif;
  font-weight: 600;
  color: #333333;
  font-size: 60px;
  line-height: 105px;
}

.cover-box .text p:nth-child(2) {
  margin-left: 103px;
}

.cover-box .text p:last-child {
  font-size: 80px;
  line-height: 156px;
  margin-left: 22px;
}

.cover-box .desc {
  top: 500px;
  left: 102px;
  width: 390px;
  margin-bottom: 7px;
  font-weight: 500;
  font-size: 30px;
  line-height: 40px;
}

.cover-box .btn {
  display: inline-block;
  width: 381px;
  height: 81px;
  line-height: 81px;
  text-align: center;
  left: 117px;
  top: 650px;
  background: #18a5ca;
  border-radius: 50px;
  font-weight: 700;
  font-size: 40px;
  color: #fff;
}

.quie-and-reply {
  display: inline-block;
  text-align: center;
  width: 462px;
  height: 95px;
  margin: 133px auto 93px;
  background: #ecc331;
  border-radius: 50px;
  font-weight: 700;
  font-size: 40px;
  line-height: 95px;
  text-transform: uppercase;
  color: #ffffff;
}

.list {
  display: inline-block;
}

.list .list-item {
  width: 1170px;
  height: 160px;
  margin-bottom: 81px;
  background: #f1f0ff;
  border-radius: 20px;
  filter: drop-shadow(4px 4px 10px rgba(0, 0, 0, 0.25));
}

.list .list-item .img {
  width: 273px;
  height: 160px;
  background: #d9d9d9;
  border-radius: 20px;
}

.list .list-item .right {
  padding: 37px 27px;
}

.list .list-item .right .bar .tag {
  width: 96px;
  height: 28px;
  border-radius: 24px;
  font-weight: 700;
  font-size: 16px;
  line-height: 28px;
  text-transform: uppercase;
  color: #ffffff;
}

.list .list-item .right .bar .warp {
  width: 422px;
  height: 24px;
  margin-right: 48px;
}

.list .list-item .right .bar .warp span {
  font-size: 14px;
  color: rgba(51, 51, 51, 0.50133);
}

.list .list-item .right h2 {
  text-align: start;
  font-weight: 700;
  font-size: 24px;
  color: #333333;
  margin-top: 20px;
}
</style>