class FriendCmdAction:
    def __init__(self):
        super().__init__()

    ICommandFunction<AuthSession, ResponseData<EAllError>, AddFriendForm> addFriend = (AuthSession ss, ResponseData<EAllError> res, AddFriendForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        List<IdName> addedFriend = new ArrayList<>();
        for(IdName friend : form.getFriendList()) {
            if( friendCommonRepository.addFriend(form.getScode(), userId, friend.getUserId(), friend.getUserName(), form.getFriendType()) == true)
                addedFriend.add(new FriendForm().new IdName(friend.getUserId(), friend.getUserName()));
        }
        return res.setError(EAllError.ok).setParam("result", addedFriend);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, DelFriendForm> delFriend = (AuthSession ss, ResponseData<EAllError> res, DelFriendForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        List<String> deletedFriend = new ArrayList<>();
        for(String friendId : form.getFriendIds())
            if(friendCommonRepository.deleteFriend(form.getScode(), userId, friendId) == true)
                deletedFriend.add(friendId);
        return res.setError(EAllError.ok).setParam("result", deletedFriend);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, ChangeFriendType> changeFriendType = (AuthSession ss, ResponseData<EAllError> res, ChangeFriendType form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        List<String> updatedFriend = new ArrayList<>();

        for(NameType friend : form.getFriendTypeList()) {
            String friendId = userCommonRepository.findUserIdByUserName(form.getScode(), friend.getUserName());
            if(friendCommonRepository.updateFriendType(form.getScode(), userId, friendId, friend.getFriendType())==true)
                updatedFriend.add(friend.getUserName());
        }
        return res.setError(EAllError.ok).setParam("result", updatedFriend);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, FriendIdListForm> friendsIdList = (AuthSession ss, ResponseData<EAllError> res, FriendIdListForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        List<FriendRec> friendList = friendCommonRepository.getFriendList(form.getScode(), userId, form.getFriendType(), form.getOffset(), form.getCount());
        if(friendList.size()<1)
            return res.setError(EAllError.eNoListData);
        return res.setError(EAllError.ok).setParam("result", friendList);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, FriendCountForm> friendsCount = (AuthSession ss, ResponseData<EAllError> res, FriendCountForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());

        int count = friendCommonRepository.getFriendCount(form.getScode(), userId, form.getFriendType());
        return res.setError(EAllError.ok).setParam("type", form.getFriendType()).setParam("count", count);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, FriendInfoForm> friendsInfo = (AuthSession ss, ResponseData<EAllError> res, FriendInfoForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        List<FriendRec> friendList = friendCommonRepository.getFriendListByIds(form.getScode(), userId, form.getFriendIds());
        if(friendList.size()<1)
            return res.setError(EAllError.eNoListData);
        return res.setError(EAllError.ok).setParam("result", friendList);
    };

    ICommandFunction<AuthSession, ResponseData<EAllError>, AppendMeForm> friendMeUser = (AuthSession ss, ResponseData<EAllError> res, AppendMeForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        List<FriendRec.FriendRecInfo> friendInfoList = friendCommonRepository.getFriendMeList(form.getScode(), userId, form.getFriendType(), form.getOffset(), form.getCount());
        if(friendInfoList.size()<1)
            return res.setError(EAllError.eNoListData);

        return res.setError(EAllError.ok).setParam("result", friendInfoList);
    };

    /**
     * user list of append me by friend
     * @param ss
     * @param res
     * @param userData,
     * @return  count
     */
    ICommandFunction<AuthSession, ResponseData<EAllError>, FriendNameForm> appendMeCount = (AuthSession ss, ResponseData<EAllError> res, FriendNameForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        int count = friendCommonRepository.getFriendMeCount(form.getScode(), userId, EFriendType.friend);
        return res.setError(EAllError.ok).setParam("count", count);
    };

    /**
     * user list of block me by friend
     * @param ss
     * @param res
     * @param userData,
     * @return count
     */
    ICommandFunction<AuthSession, ResponseData<EAllError>, FriendNameForm> blockMeCount = (AuthSession ss, ResponseData<EAllError> res, FriendNameForm form) -> {
        String userId = userCommonRepository.findUserIdByUserName(form.getScode(), form.getUserName());
        int count = friendCommonRepository.getFriendMeCount(form.getScode(), ss.getUserId(), EFriendType.block);
        return res.setError(EAllError.ok).setParam("count", count);
    };