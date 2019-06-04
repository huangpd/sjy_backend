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
                <el-breadcrumb-item>{{ this.company_msg.name }}</el-breadcrumb-item>
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
                      <td colspan="3">{{ this.company_msg.name }}</td>
                    </tr>
                    <tr>
                      <td class="tb">企业类型:</td>
                      <td>{{ this.company_msg.econKind }}</td>
                      <td class="tb">统一信用代码:</td>
                      <td>{{ this.company_msg.code }}</td>
                    </tr>
                    <tr>
                      <td class="tb">注册资本:</td>
                      <td>{{ this.company_msg.registCapi }}</td>
                      <td class="tb">实缴资本:</td>
                      <td>{{ this.company_name }}</td>
                    </tr>
                    <tr>
                      <td class="tb">联系人:</td>
                      <td>{{ this.company_msg.username }}</td>
                      <td class="tb">联系电话:</td>
                      <td>{{ this.company_msg.phone }}</td>
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
                  <table
                    class="ntable"
                    style="border-spacing: 0;border-collapse: collapse;width: 100%;
                    margin: 0 auto;padding: 0;"
                  >
                    <tr>
                      <td class="tb">经营状态:</td>
                      <td>{{ this.company_msg.status }}</td>
                      <td class="tb">注册资本:</td>
                      <td>{{ this.company_msg.registCapi }}</td>
                    </tr>
                    <tr>
                      <td class="tb">法人代表:</td>
                      <td colspan="3">{{ this.company_msg.operName }}</td>
                    </tr>
                    <tr>
                      <td class="tb">注册地址:</td>
                      <td colspan="3">{{ this.company_msg.address }}</td>
                    </tr>
                    <tr>
                      <td class="tb">注册时间:</td>
                      <td>{{ this.company_msg.startDate }}</td>
                      <td class="tb">类型:</td>
                      <td>{{ this.company_msg.econKind }}</td>
                    </tr>
                    <tr>
                      <td class="tb">经营范围:</td>
                      <td colspan="3">{{ this.company_msg.scope }}</td>
                    </tr>
                  </table>
                </el-tab-pane>

                <el-tab-pane name="second">
                  <div slot="label">
                    <span>纳税情况</span>
                  </div>
                  <table class="gridtable">
                    <tr>
                      <th>年度</th>
                      <th>增值税(万元)</th>
                      <th>企业所得税(万元)</th>
                      <th>个税(万元)</th>
                      <th>税收留存(万元)</th>
                      <th>税收奖励(万元)</th>
                    </tr>
                    <tr v-for="v in tax_list" v-bind:key="v.id">
                      <td v-text="v.year"></td>
                      <td v-text="v.zengzhi_tax"></td>
                      <td v-text="v.company_tax"></td>
                      <td v-text="v.personal_tax"></td>
                      <td v-text="v.total_tax"></td>
                      <td v-text="v.bonus_tax"></td>
                    </tr>
                  </table>
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

                  <el-table border :data="this.shareholderInfo_list" style="width: 100%">
                    <el-table-column
                      v-for="col in this.shareholderInfo_cols"
                      stripe
                      :prop="col.key"
                      :label="col.title"
                      :width="col.width"
                      :key="col.id"
                    ></el-table-column>
                  </el-table>
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

                  <el-table border :data="this.businessChange_list" style="width: 100%">
                    <el-table-column
                      v-for="col in this.businessChange_cols"
                      stripe
                      :prop="col.key"
                      :label="col.title"
                      :width="col.width"
                      :key="col.id"
                    ></el-table-column>
                  </el-table>
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

                  <el-table border :data="this.abnormalInfo_list" style="width: 100%">
                    <el-table-column
                      v-for="col in this.abnormalInfo_cols"
                      stripe
                      :prop="col.key"
                      :label="col.title"
                      :width="col.width"
                      :key="col.id"
                    ></el-table-column>
                  </el-table>
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

                  <el-table border :data="this.legalAction_list" style="width: 100%">
                    <el-table-column
                      v-for="col in this.legalAction_cols"
                      stripe
                      :prop="col.key"
                      :label="col.title"
                      :width="col.width"
                      :key="col.id"
                    ></el-table-column>
                  </el-table>
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
import api from "@/utils/api";
import companyDetails_data from "@/utils/companyDetails_data";
import http from "@/utils/http";

export default {
  name: "CompanyDetails",
  data() {
    return {
      id: this.$route.params.id,
      company_msg: {
        name: "",
        code: "",
        econKind: "",
        address: "",
        operName: "",
        registCapi: "",
        scope: "",
        startDate: "",
        status: "",
        username: "",
        phone: ""
      }, //公司名
      company_verify: 0, //公司审核状态

      shareholderInfo_amount: 0, //股东信息消息数目
      businessChange_amount: 0, //工商变更消息数目
      abnormalInfo_amount: 0, //异常记录消息数目
      legalAction_amount: 0, //法律诉讼消息数目

      shareholderInfo_cols: companyDetails_data.shareholder_cols, //股东信息表头
      businessChange_cols: companyDetails_data.businessChange_cols, //工商变更表头
      abnormalInfo_cols: companyDetails_data.abnormalInfo_cols, //异常记录表头
      legalAction_cols: companyDetails_data.legalAction_cols, //法律诉讼表头

      taxInfo_list: [], //纳税情况
      shareholderInfo_list: [], //股东信息
      businessChange_list: [], //工商变更
      abnormalInfo_list: [], //异常记录
      legalAction_list: [] //法律诉讼
    };
  },
  methods: {
    get_data: async function() {
      let params = { id: this.id };
      const res = await http.post(api.company_query, params);
      if (res.data) {
        let company_data = res.data;
        this.company_msg = {
          name: company_data.Name,
          code: company_data.Code,
          econKind: company_data.EconKind,
          address: company_data.Address,
          operName: company_data.OperName,
          registCapi: company_data.RegistCapi,
          scope: company_data.Scope,
          status: company_data.Status,
          startDate: company_data.StartDate
        };
        this.shareholderInfo_list = company_data.shareholderInfo_list;
        this.businessChange_list = company_data.businessChange_list;
        this.abnormalInfo_list = company_data.abnormalInfo_list;
        this.legalAction_list = company_data.legalAction_list;
        console.log(this.shareholderInfo_list)

        this.shareholderInfo_amount = this.shareholderInfo_list.length;
        this.businessChange_amount = this.businessChange_list.length;
        this.abnormalInfo_amount = this.abnormalInfo_list.length;
        this.legalAction_amount = this.legalAction_list.length;
      }
    }
  },
  created() {
    this.get_data();
  }
};
</script>

<style  scoped>
.gridtable {
  font-family: verdana, arial, sans-serif;
  font-size: 16px;
  color: #333333;
  border-width: 5px;
  border: 5px;
  border-color: #666666;
  border-collapse: collapse;
  margin: 15px auto;
  width: 80%;
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
  width: auto;
}
table td {
  padding: 12px 10px 12px 10px;
  border: #e4eef6 1px solid;
  word-break: keep-all;
  font-size: 14px;
  line-height: 19px;
  color: #222;
}
.item {
  margin-top: auto;
}
</style>