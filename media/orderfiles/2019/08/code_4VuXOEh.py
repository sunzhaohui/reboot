# -*- coding: utf-8 -*-

class WorkOrderApplyView(LoginRequiredMixin, View):
    def get(self, request):
        forms = WorkOrderApplyForm()
        return render(request, 'order/workorder_apply.html', {'forms': forms})

    def post(self, request):
        forms = WorkOrderApplyForm(request.POST or None, request.FILES or None)
        if forms.is_valid():
            try:
                print(forms.cleaned_data)
                title = forms.cleaned_data["title"]
                order_contents = forms.cleaned_data["order_contents"]
                assign = forms.cleaned_data["assign"]
                orderfiles = forms.cleaned_data["orderfiles"]

                work_order = WorkOrder()
                work_order.title = title
                work_order.order_contents = order_contents
                work_order.assign_id = assign
                work_order.orderfiles = orderfiles
                work_order.applicant = request.user
                work_order.status = 0
                work_order.save()
                return HttpResponseRedirect(reverse('workorder:list'))
            except:
                return render(request, 'order/workorder_apply.html', {'forms': forms, 'errmsg': '工单提交出错！'})
        else:
            return render(request, 'order/workorder_apply.html', {'forms': forms, 'errmsg': '工单填写格式出错！'})
