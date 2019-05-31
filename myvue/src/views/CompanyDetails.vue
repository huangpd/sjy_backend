<template>
  <el-container>
    <el-main>
      <el-row type="flex" justify="space-around">
        <el-col :span="20">
          <el-row>
            <el-col>
              <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: '/town_home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>
                  <a href="/town_company">企业列表</a>
                </el-breadcrumb-item>
                <el-breadcrumb-item>{{ this.company_name }}</el-breadcrumb-item>
              </el-breadcrumb>
            </el-col>
          </el-row>

          <el-row :gutter="24">
            <el-col :span="16">
              <el-card class="box-card">
                <el-row>
                  <table class="ntable">
                    <tr>
                      <td class="tb">企业全称:</td>
                      <td colspan="3">{{ fullname }}</td>
                    </tr>
                    <tr>
                      <td class="tb">企业类型:</td>
                      <td>{{ this.company_name }}</td>
                      <td class="tb">统一信用代码:</td>
                      <td>{{ this.company_name }}</td>
                    </tr>
                    <tr>
                      <td class="tb">注册资本:</td>
                      <td>{{ this.company_name }}</td>
                      <td class="tb">实缴资本:</td>
                      <td>{{ this.company_name }}</td>
                    </tr>
                    <tr>
                      <td class="tb">联系人:</td>
                      <td>{{ this.company_name }}</td>
                      <td class="tb">联系电话:</td>
                      <td>{{ this.company_name }}</td>
                    </tr>
                    <tr>
                      <td class="tb">邮箱:</td>
                      <td colspan="3">{{ this.company_name }}</td>
                    </tr>
                  </table>
                </el-row>
                <el-row type="flex" justify="center" class="row-bg">
                  <el-button v-if="company_verify" type="danger" plain>取消通过</el-button>
                  <el-button v-else type="success" plain>通过审核</el-button>
                </el-row>
              </el-card>
            </el-col>
            <el-col :span="6" :offset="2">
              <div class="block">
                <span class="demonstration">营业执照未上传</span>
                <el-image>
                  <div slot="error" class="image-slot">
                    <i class="el-icon-picture-outline"></i>
                  </div>
                </el-image>
              </div>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="20">
              <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
                <el-tab-pane name="first">
                  <div slot="label">
                    <span>工商信息</span>
                  </div>
                </el-tab-pane>

                <el-tab-pane name="second">
                  <div slot="label">
                    <span>纳税情况</span>
                  </div>
                </el-tab-pane>

                <el-tab-pane>
                  <div slot="label">
                    <span>股东信息</span>
                    <el-badge
                      v-if="this.shareholderInfo_amount"
                      :value="this.shareholderInfo_amount"
                      class="item"
                      type="primary"
                    />
                  </div>
                </el-tab-pane>

                <el-tab-pane name="fourth">
                  <div slot="label">
                    <span>工商变更</span>
                    <el-badge
                      v-if="this.businessChange_amount"
                      :value="this.businessChange_amount"
                      class="item"
                      type="primary"
                    />
                  </div>
                </el-tab-pane>

                <el-tab-pane name="fifth">
                  <div slot="label">
                    <span>异常记录</span>
                    <el-badge
                      v-if="this.abnormalInfo_amount"
                      :value="this.abnormalInfo_amount"
                      class="item"
                      type="primary"
                    />
                  </div>
                </el-tab-pane>

                <el-tab-pane name="sixth">
                  <div slot="label">
                    <span>法律诉讼</span>
                    <el-badge
                      v-if="this.legalAction_amount"
                      :value="this.legalAction_amount"
                      class="item"
                      type="primary"
                    />
                  </div>
                </el-tab-pane>
              </el-tabs>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import countTo from "vue-count-to";
import api from "@/utils/api";
import companyDetails_data from "@/utils/companyDetails_data";

export default {
  name: "CompanyDetails",
  components: { countTo },
  data() {
    return {
      company_name: "test", //公司名
      company_verify: 0, //公司审核状态
      businessInfo_amount: 0, //工商信息消息数目
      taxInfo_amount: 0, //纳税情况消息数目
      shareholderInfo_amount: 2, //股东信息消息数目
      businessChange_amount: 1, //工商变更消息数目
      abnormalInfo_amount: 4, //异常记录消息数目
      legalAction_amount: 5, //法律诉讼消息数目
      fullname: companyDetails_data.full_name //公司全称
    };
  }
};
// console.log(this.shareholderInfo)
</script>

<style  scoped>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.ntable {
  border-spacing: 0;
  border-collapse: collapse;
  width: 90%;
  margin: 20px auto;
  padding: 20px;
}
table .tb {
  background: #f2f9fc;
}
table td {
  padding: 12px 10px 12px 10px;
  border: #e4eef6 1px solid;
  word-break: break-all;
  font-size: 14px;
  line-height: 19px;
  color: #222;
}
.item {
  margin-top: auto;
}
</style>