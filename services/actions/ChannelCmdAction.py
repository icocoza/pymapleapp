class ChannelCmdAction:
    def __init__(self):
        super().__init__()

   ICommandFunction<AuthSession, ResponseData<EAllError>, ChannelCreateForm> channelCreate = (AuthSession ss, ResponseData<EAllError> res, ChannelCreateForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        int attendeeCount = 2;
        if(form.getAttendees().size() > 1) {
            form.getAttendees().add(userId);
            attendeeCount++;
        }else {
            ChannelRec rec = channelCommonRepository.findChatChannel(form.getScode(), userId, form.getAttendees().get(0));
            if( rec != ChannelRec.Empty ) {
                channelCommonRepository.addMyChannel(form.getScode(), userId, rec.getChannelId());
                return res.setError(EAllError.ok).setParam(rec.getChannelId());
            }
        }

        String channelId = StrUtils.getSha1Uuid("channel:");
        String strAttendees = form.getAttendees().stream().collect(Collectors.joining(AsciiSplitter.ASS.RECORD));
        channelCommonRepository.addChatChannel(form.getScode(), channelId, userId, strAttendees, attendeeCount, attendeeCount == 2? EChannelType.oneToOne : EChannelType.group);
        channelCommonRepository.addMyChannel(form.getScode(), userId, channelId);

        return res.setError(EAllError.ok).setParam(channelId);
    };


    ICommandFunction<AuthSession, ResponseData<EAllError>, ChannelExitForm> channelExit = (AuthSession ss, ResponseData<EAllError> res, ChannelExitForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        ChannelRec rec = channelCommonRepository.getChatChannel(form.getScode(), form.getChannelId());
        if( rec == ChannelRec.Empty )
            return res.setError(EAllError.eNoChannel);

        channelCommonRepository.delMyChannel(form.getScode(), userId, form.getChannelId());
        if( rec.getChannelType() == EChannelType.group ) {
            if( rec.getAttendees().contains(userId) == true)
                rec.setAttendees(rec.getAttendees().replace(userId+ AsciiSplitter.ASS.RECORD, "").replace(userId, ""));
            if(rec.getAttendees().length() < 1)
                channelCommonRepository.delChatChannel(form.getScode(), form.getChannelId());
            else
                channelCommonRepository.updateChatChannelAttendee(form.getScode(), form.getChannelId(), rec.getAttendees(), rec.getAttendeeCount()-1);
        }
        return res.setError(EAllError.ok).setParam("channelId", form.getChannelId()).setParam("attendees", rec.getAttendees());
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, ChannelEnterForm> channelEnter = (AuthSession ss, ResponseData<EAllError> res, ChannelEnterForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        ChannelRec rec = channelCommonRepository.getChatChannel(form.getScode(), form.getChannelId());
        if(rec == ChannelRec.Empty)
            return res.setError(EAllError.eNoChannel);

        channelCommonRepository.addMyChannel(form.getScode(), userId, form.getChannelId());
        return res.setError(EAllError.ok).setParam("channelId", form.getChannelId());
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, ChannelInviteForm> channelInvite = (AuthSession ss, ResponseData<EAllError> res, ChannelInviteForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        ChannelRec rec = channelCommonRepository.getChatChannel(form.getScode(), form.getChannelId());
        if(rec == ChannelRec.Empty)
            return res.setError(EAllError.eNoChannel);

        for(String attendeeId : form.getAttendees()) {
            if(rec.getAttendees().contains(attendeeId) == false) {
                rec.setAttendees(rec.getAttendees() + AsciiSplitter.ASS.RECORD + attendeeId);
                rec.setAttendeeCount(rec.getAttendeeCount() + 1);
                rec.setChannelType(EChannelType.group);
            }
        }

        if(rec.getChannelType() == EChannelType.group && rec.getAttendees().contains(userId)==false)
            rec.setAttendees(rec.getAttendees() + AsciiSplitter.ASS.RECORD + userId);

        if(channelCommonRepository.updateChatChannelAttendee(form.getScode(), form.getChannelId(), rec.getAttendees(), rec.getAttendeeCount(), rec.getChannelType())==false)
            return res.setError(EAllError.eFailToUpdate);
        return res.setError(EAllError.ok).setParam("channelId", form.getChannelId()).setParam("attendees", rec.getAttendees());
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, MyChannelForm> myChannel = (AuthSession ss, ResponseData<EAllError> res, MyChannelForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        List<MyChannelRec> channelList =  channelCommonRepository.getMyChannelList(form.getScode(), userId, form.getOffset(), form.getCount());
        if(channelList.size() < 1)
            return res.setError(EAllError.eNoListData);

        return res.setError(EAllError.ok).setParam("channelList", channelList);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, UserForm.FindIdForm> myChannelCount = (AuthSession ss, ResponseData<EAllError> res, UserForm.FindIdForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        int count = channelCommonRepository.getMyChannelCount(form.getScode(), userId);
        return res.setError(EAllError.ok).setParam("channelCount", count);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, ChannelLastMessageForm> channelLastMessage = (AuthSession ss, ResponseData<EAllError> res, ChannelLastMessageForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        List<ChannelRec.RecChLastMsg> lastMessageList = channelCommonRepository.getChannelLastMsg(form.getScode(), form.getChannelIds());
        return res.setError(EAllError.ok).setParam("result", lastMessageList);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, ChannelInfoForm> channelInfos = (AuthSession ss, ResponseData<EAllError> res, ChannelInfoForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        List<MyChannelRec.MyChannelRecExt> channelList = channelCommonRepository.getMyChannelInfoList(form.getScode(), userId, form.getOffset(), form.getCount());
        return res.setError(EAllError.ok).setParam("result", channelList);
    };