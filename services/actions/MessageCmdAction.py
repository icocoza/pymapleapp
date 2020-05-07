class MessageCmdAction:
    def __init__(self):
        super().__init__()

    ICommandFunction<AuthSession, ResponseData<EAllError>, ChatMessageForm> message = (AuthSession ss, ResponseData<EAllError> res, ChatMessageForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        String messageId = StrUtils.getSha1Uuid("messageId:");

        if(messageCommonRepository.addChatMessage(form.getScode(), messageId, form.getChannelId(), userId, form.getMessageType(), form.getContent()) == false)
            return res.setError(EAllError.eFailToSaveMessage);
        if(channelCommonRepository.updateChatChannelLastMsgAndTime(form.getScode(), form.getChannelId(), obtainShortcut(form.getContent())) == false)
            return res.setError(EAllError.eFailToUpdateChannel);

        return res.setError(EAllError.ok).setParam("messageId", messageId).setParam("content", form.getContent());
    };

    private String obtainShortcut(String msg) {
        return msg.length()>32 ? msg.substring(0, 31) : msg;
    }

    ICommandFunction<AuthSession, ResponseData<EAllError>, SyncMessageForm> syncMessage = (AuthSession ss, ResponseData<EAllError> res, SyncMessageForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        MyChannelRec rec = channelCommonRepository.getMyChannel(form.getScode(), userId, form.getChannelId());
        if( rec == MyChannelRec.Empty )
            return res.setError(EAllError.eNoChannel);

        List<MessageDelRec.RecDelId> delList = messageCommonRepository.getDelMessageIdList(form.getScode(), form.getChannelId(), userId, rec.getCreatedAt());

        List<MessageRec> msgList = new ArrayList<>();
        if(delList.size() < 1)
            msgList.addAll(messageCommonRepository.getChatMessageList(form.getScode(), form.getChannelId(), rec.getCreatedAt(), form.getOffset(), form.getCount()));
        else {
            String deletedIds = delList.stream().map(e -> "'" + e.messageId + "'").collect(Collectors.joining(","));
            msgList.addAll(messageCommonRepository.getMessageListWithoutDeletion(form.getScode(), form.getChannelId(), rec.getCreatedAt(), deletedIds, form.getOffset(), form.getCount()));
        }

        return res.setError(EAllError.ok).setParam("channelId", form.getChannelId()).setParam("result", msgList);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, MessageIdForm> onlineOnlyMessage = (AuthSession ss, ResponseData<EAllError> res, MessageIdForm form) -> {
        return res.setError(EAllError.eNoServiceCommand);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, MessageIdForm> pushOnlyMessage = (AuthSession ss, ResponseData<EAllError> res, MessageIdForm form) -> {
        return res.setError(EAllError.eNoServiceCommand);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, ReadMessageForm> readMessage = (AuthSession ss, ResponseData<EAllError> res, ReadMessageForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        MyChannelRec rec = channelCommonRepository.getMyChannel(form.getScode(), userId, form.getChannelId());
        if(rec == MyChannelRec.Empty)
            return res.setError(EAllError.eNoChannel);

        List<MessageRec> messageList = messageCommonRepository.getChatMessageList(form.getScode(), form.getChannelId(), form.getMessageIds());
        if(messageList.size() < 1)
            return res.setError(EAllError.eNoMessage);

        for( MessageRec item : messageList ) {
            messageCommonRepository.addMessageReadInfo(form.getScode(), form.getChannelId(), userId, item.getMessageId());
            messageCommonRepository.incReadCount(form.getScode(), item.getMessageId());
        }
        List<String> messageIds = messageList.stream().map(x -> x.getMessageId()).collect(Collectors.toList());
        return res.setError(EAllError.ok).setParam("channelId", form.getChannelId()).setParam("readIdList", messageIds);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, DelMessageForm> delMessage = (AuthSession ss, ResponseData<EAllError> res, DelMessageForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        List<String> deletedIds = new ArrayList<>();
        for(String messageId : form.getMessageIds()) {
            if (messageCommonRepository.addDelMessageId(form.getScode(), form.getChannelId(), userId, messageId) == true)
                deletedIds.add(messageId);
        }

        if(deletedIds.size() < 1)
            return res.setError(EAllError.eFailToDeleteMessage);
        return res.setError(EAllError.ok).setParam("channelId", form.getChannelId()).setParam("deletedIdList", deletedIds);
    };