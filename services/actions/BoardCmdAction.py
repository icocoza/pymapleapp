import os, sys, json, datetime
from services.constant.MapleCmd import EBoardCmd
import common.utils.StrUtils as StrUtils
from common.utils.ImageTool import ImageTool
from services.constant.AllError import AllError
from services.actions.Action import Action

from repository.db.user.UserRepository import UserRepository
from repository.db.board.BoardContentRepository import BoardContentRepository
from repository.db.board.BoardCountRepository import BoardCountRepository
from repository.db.board.BoardDetailRepository import BoardDetailRepository
from repository.db.board.BoardLikeRepository import BoardLikeRepository
from repository.db.board.BoardReplyRepository import BoardReplyRepository
from repository.db.board.BoardRepository import BoardRepository
from repository.db.board.BoardScrapRepository import BoardScrapRepository
from repository.db.board.BoardVoteItemRepository import BoardVoteItemRepository
from repository.db.board.BoardVoteRepository import BoardVoteRepository
from repository.db.board.BoardVoteUserCountRepository import BoardVoteUserCountRepository
from repository.db.board.BoardVoteUserRepository import BoardVoteUserRepository
from repository.db.board.ScrapBodyRepository import ScrapBodyRepository
from repository.db.board.ScrapDetailRepository import ScrapDetailRepository
from repository.db.board.ScrapRepository import ScrapRepository
from repository.db.file.FileRepository import FileRepository

from common.utils.HtmlScrapper import HtmlScrapper
from services.constant.MapleEnum import EBoardContentType
import common.config.appconfig as appconfig
class BoardCmdAction(Action):

    def __init__(self):
        super().__init__()

        self.userRepository = UserRepository()
        self.boardContentRepository = BoardContentRepository()
        self.boardCountRepository = BoardCountRepository()
        self.boardDetailRepository = BoardDetailRepository()
        self.boardLikeRepository = BoardLikeRepository()
        self.boardReplyRepository = BoardReplyRepository()
        self.boardRepository = BoardRepository()
        self.boardScrapRepository = BoardScrapRepository()
        self.boardVoteItemRepository = BoardVoteItemRepository()
        self.boardVoteRepository = BoardVoteRepository()
        self.boardVoteUserCountRepository = BoardVoteUserCountRepository()
        self.boardVoteUserRepository = BoardVoteUserRepository()
        self.scrapBodyRepository = ScrapBodyRepository()
        self.scrapDetailRepository = ScrapDetailRepository()
        self.scrapRepository = ScrapRepository()
        self.fileRepository = FileRepository()
        
        self.funcMap = {}
        self.funcMap[EBoardCmd.addBoard.name] = lambda scode, session, jdata: self.addBoard(scode, session, jdata)
        self.funcMap[EBoardCmd.delBoard.name] = lambda scode, session, jdata: self.delBoard(scode, session, jdata)
        self.funcMap[EBoardCmd.updateBoardTitle.name] = lambda scode, session, jdata: self.updateBoardTitle(scode, session, jdata)
        self.funcMap[EBoardCmd.updateBoardContent.name] = lambda scode, session, jdata: self.updateBoardContent(scode, session, jdata)
        self.funcMap[EBoardCmd.updateBoardCategory.name] = lambda scode, session, jdata: self.updateBoardCategory(scode, session, jdata)
        self.funcMap[EBoardCmd.updateBoard.name] = lambda scode, session, jdata: self.updateBoard(scode, session, jdata)
        self.funcMap[EBoardCmd.getBoardList.name] = lambda scode, session, jdata: self.getBoardList(scode, session, jdata)
        self.funcMap[EBoardCmd.getBoardContent.name] = lambda scode, session, jdata: self.getBoardContent(scode, session, jdata)
        self.funcMap[EBoardCmd.incBoardLike.name] = lambda scode, session, jdata: self.incBoardLike(scode, session, jdata)
        self.funcMap[EBoardCmd.incBoardDislike.name] = lambda scode, session, jdata: self.incBoardDislike(scode, session, jdata)

        self.funcMap[EBoardCmd.addReply.name] = lambda scode, session, jdata: self.addReply(scode, session, jdata)
        self.funcMap[EBoardCmd.delReply.name] = lambda scode, session, jdata: self.delReply(scode, session, jdata)
        self.funcMap[EBoardCmd.replyList.name] = lambda scode, session, jdata: self.replyList(scode, session, jdata)
        self.funcMap[EBoardCmd.addVote.name] = lambda scode, session, jdata: self.addVote(scode, session, jdata)
        self.funcMap[EBoardCmd.voteItemList.name] = lambda scode, session, jdata: self.voteItemList(scode, session, jdata)
        self.funcMap[EBoardCmd.selectVoteItem.name] = lambda scode, session, jdata: self.selectVoteItem(scode, session, jdata)

        self.funcMap[EBoardCmd.updateVote.name] = lambda scode, session, jdata: self.updateVote(scode, session, jdata)
        self.funcMap[EBoardCmd.changeVoteSelection.name] = lambda scode, session, jdata: self.changeVoteSelection(scode, session, jdata)
        self.funcMap[EBoardCmd.getVoteInfoList.name] = lambda scode, session, jdata: self.getVoteInfoList(scode, session, jdata)

        self.imageTool = ImageTool()

    def __addBoard(self, scode, userId, userName, jdata, scrapIds):
        boardId = StrUtils.getMapleUuid('boardId:')

        userRec = self.userRepository.getUser(scode, userId)
        if userRec == None or userRec['leftAt'] != None:
            return self.setError(scode, AllError.InvalidUser)
        if self.boardRepository.insert(scode, boardId, userId, userName, jdata['title'], self._getShortContent(jdata['content']), 
                                       jdata['hasImage'], jdata['hasFile'], jdata['category'], jdata['contentType'] if 'contentType' not in jdata else 'text') == False:
            return self.setError(scode, AllError.FailAddBoard)
        
        self.boardContentRepository.insert(scode, boardId, userId, jdata['content'])
        self.boardCountRepository.insert(scode, boardId)

        queries = []        
        if scrapIds is not None and len(scrapIds) > 0:
            for scrapId in scrapIds:
                queries.append(self.boardScrapRepository.qInsertScrap(scode, boardId, scrapId))
        self.boardScrapRepository.multiQueries(scode, queries)

        if 'fileIds' in jdata and len(jdata['fileIds']) > 0:
            self.uploadFileRepository.updateFilesEnabled(scode, jdata['fileIds'], boardId, True)
            fileRec = self.uploadFileRepository.getFile(scode, jdata['fileIds'][0])
            
            if self.imageTool.cropImageByFilename(scode, userId, appconfig.upload_path, fileRec['fileName'], appconfig.crop_path):
                self.fileRepository.updateCropped(scode, fileRec['fileId'], True)

        return self.setOk(scode, {'boardId': boardId})

    def __findAndAddScrap(self, scode, userId, jdata):
        htmlScrapper = HtmlScrapper()
        urls = StrUtils.extractUrls(jdata['content'])
        if len(urls) < 1 :
            return
        scrapIds = []
        for url in urls:
            if self.scrapRepository.getScrapListByUrl(scode, url) != None:
                continue
            title, subtitle, body, img_url = htmlScrapper.scrap(url)
            if title is None:
                continue
            scrapId = StrUtils.getMapleUuid('scrapId:')
            queries = []
            queries.append(self.scrapRepository.qInsertScrap(scode, scrapId, url, title, subtitle))
            queries.append(self.scrapBodyRepository.qInsertScrapBody(scode, scrapId, body))
            self.scrapBodyRepository.multiQueries(scode, queries)

            ### Image Crop and Insert DB 
            ### filePath = millisecond +'-'+ original filename
            filePath, fileSize = ImageTool.download(scode, userId, img_url, appconfig.scrap_path)
            if filePath is not None:
                ImageTool.cropImageByFullPath(scode, userId, filePath, appconfig.crop_path)
                fileName = filePath.split('/')[-1]
                self.scrapRepository.updateScrapFile(scode, scrapId, fileName)
            scrapIds.append(scrapId)
        return scrapIds

    def addBoard(self, scode, session, jdata):
        userId = session['userId']
        userName = session['userName']

        scrapIds = self.__findAndAddScrap(scode, userId, jdata)
        return self.__addBoard(scode, userId, userName, jdata, scrapIds)

    def delBoard(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']
        if self.boardRepository.updateDelete(scode, boardId, userId) == False:
            return self.setError(scode, AllError.FailDeleteBoard)
        return self.setOk(scode, {'boardId': boardId})

    def updateBoardTitle(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']
        if self.boardRepository.updateTitle(scode, boardId, userId, jdata['title']) == False:
            return self.setError(scode, AllError.FailUpdate)
        return self.setOk(scode, {'boardId': boardId})

    def updateBoardContent(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']
        if self.boardRepository.updateContent(scode, boardId, userId, jdata['content'], jdata['hasImage'], jdata['hasFile']) == False:
            return self.setError(scode, AllError.FailUpdate)
        self.boardContentRepository.updateContent(scode, boardId, userId, jdata['content'])
        return self.setOk(scode, {'boardId': boardId})

    def updateBoardCategory(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']
        if self.boardRepository.updateCategory(scode, boardId, userId, jdata['category']) == False:
            return self.setError(scode, AllError.FailUpdate)
        return self.setOk(scode, {'boardId': boardId})

    def __udpateBoard(self, scode, userId, boardId, scrapIds, jdata):
        if self.boardRepository.updateBoard(scode, boardId, userId, jdata['title'], self._getShortContent(jdata['content']), 
                    jdata['hasFile'], jdata['category'], jdata['contentType']) == False:
            return self.setError(scode, AllError.FailUpdate)
        
        self.boardContentRepository.updateContent(scode, boardId, userId, jdata['content'])
        self.uploadFileRepository.updateDeleteFile(scode, boardId)
        self.uploadFileRepository.updateFileEnabled(scode, jdata['fileIds'], boardId, True)
        self.boardScrapRepository.delete(scode, boardId)

        queries = []
        for scrapId in scrapIds:
            queries.append(self.boardScrapRepository.qInsertScrap(scode, boardId, scrapId))
        self.boardScrapRepository.multiQueries(scode, queries)

        return self.setOk(scode, {'boardId': boardId})

    def updateBoard(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']

        scrapIds = self.__findAndAddScrap(scode, jdata)
        return self.__udpateBoard(scode, userId, boardId, scrapIds, jdata)
    
    def getBoardList(self, scode, session, jdata):
        userId = session['userId']
        boardList = self.boardDetailRepository.getBoardList(scode, jdata['category'], jdata['offset'], jdata['count'])
        if len(boardList) < 1:
            return self.setError(scode, AllError.NoListData)
        voteBoardIds = list(filter(lambda item: item['contentType'] == EBoardContentType.vote.name, boardList))
        if len(voteBoardIds) > 0:
            voteCount = self.boardVoteUserCountRepository.getVoteCount(scode, voteBoardIds)
            if len(voteCount) > 0:
                votedIt = self.boardVoteUserCountRepository.getVotedBoardId(scode, userId, voteBoardIds)
                for board in boardList:
                    if board['contentType'] == EBoardContentType.vote.name and board['boardId'] in voteCount:
                        board['voteCount'] = voteCount['voteCount']
                    board['voted'] = True if board['boardId'] in votedIt else False

        return self.setOk(scode, boardList)
        
    def getBoardContent(self, scode, session, jdata):
        boardId = jdata['boardId']
        content = self.boardContentRepository.getContent(scode, boardId)
        if content is None:
            return self.setError(scode, AllError.NoData)        
        self.boardCountRepository.incVisit(scode, boardId)

        scrapList = self.scrapDetailRepository.getScrapDetailList(scode, boardId)
        likeRec = self.boardLikeRepository.getPreference(scode, boardId, content['userId'])
        files = self.fileRepository.getFileList(scode, boardId)
        voteItems = self.boardVoteItemRepository.getVoteItemList(scode, boardId)
        count = self.boardCountRepository.getCountInfo(scode, boardId)

        return self.setOk(scode, {'scrapList': scrapList, 'like': likeRec, 'files': files, 'voteItems': voteItems, 'count': count, 'content': content})

    def incBoardLike(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']
        if jdata['added'] == True and self.boardLikeRepository.insert(scode, boardId, userId, session['userName'], jdata['preference']) == False:
            return self.setError(scode, AllError.AlreadyLikedOrDisliked)
        elif jdata['added'] == False and self.boardLikeRepository.deletePreference(scode, boardId, userId, jdata['preference']) == False:
            return self.setError(scode, AllError.NotExistLikedUser)
        self.boardCountRepository.incLike(scode, boardId, jdata['added'])
        countRec = self.boardCountRepository.getCountInfo(scode, boardId)
        return self.setOk(scode, {'boardId': boardId, 'preference': jdata['preference'], 'added': jdata['added'], 'count': countRec})

    def incBoardDislike(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']
        if jdata['added'] == True and self.boardLikeRepository.insert(scode, boardId, userId, session['userName'], jdata['preference']) == False:
            return self.setError(scode, AllError.AlreadyLikedOrDisliked)
        elif jdata['added'] == False and self.boardLikeRepository.deletePreference(scode, boardId, userId, jdata['preference']) == False:
            return self.setError(scode, AllError.NotExistDislikeUser)
        self.boardCountRepository.incDislike(scode, boardId, jdata['added'])
        countRec = self.boardCountRepository.getCountInfo(scode, boardId)
        return self.setOk(scode, {'preference': jdata['preference'], 'added': jdata['added'], 'count': countRec})

    def addReply(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']
        replyId = StrUtils.getMapleUuid('replyId:')

        if ('parentReplyId' not in jdata or len(jdata['parentReplyId']) < 1) and ('depth' not in jdata or int(jdata['depth']) > 0):
            return self.setError(scode, AllError.ErrorReplyHierarchy)

        self.boardReplyRepository.insert(scode, replyId, boardId, jdata['parentReplyId'], userId, session['userName'], jdata['depth'], jdata['body'])
        replyList = self.boardReplyRepository.getList(scode, boardId, 0, 15)

        return self.setOk(scode, {'replyId': replyId, 'replyList': replyList})

    def delReply(self, scode, session, jdata):
        userId = session['userId']
        replyId = jdata['replyId']

        if self.boardReplyRepository.delete(scode, replyId, userId) == False:
            return self.setError(scode, AllError.FailDeleteReply)
        return self.setOk(scode, {'replyId': replyId})

    def replyList(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']

        replyList = self.boardReplyRepository.getList(scode, boardId, jdata['offset'], jdata['count'])
        return self.setOk(scode, {'replyList': replyList})

    def addVote(self, scode, session, jdata):
        if len(jdata['voteItems']) < 2:
            return self.setError(scode, AllError.VoteItemHas2More)
        res = self.addBoard(scode, session, jdata)
        if res['result'] != 'ok':
            return res
        userId = session['userId']
        boardId = res['data']['boardId']

        if self.boardVoteRepository.insert(scode, boardId, userId, session['userName'], jdata['expiredAt']) == False:
            self.boardRepository.deleteBoard(scode, boardId, userId)
            return self.setError(scode, AllError.InvalidParameter)        
        for voteItem in jdata['voteItems']:
            voteId = StrUtils.getMapleUuid('voteId:')
            self.boardVoteItemRepository.insert(scode, boardId, voteId, voteItem)        
        return self.setOk(scode, {'boardId': boardId})

    def voteItemList(self, scode, session, jdata):
        boardId = jdata['boardId']
        voteItemList = self.boardVoteItemRepository.getVoteItemList(scode, boardId)
        return self.setOk(scode, {'boardId': boardId, 'voteItems': voteItemList})

    def selectVoteItem(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']
        voteItemId = jdata['voteItemId']
        selected = jdata['selected']

        voteUser = self.boardVoteUserRepository.getVoteUser(scode, userId, boardId)
        if selected and voteUser is not None:
            return self.setError(scode, AllError.AlreadyVoteUser)
        elif selected == False and voteUser is None:
            return self.setError(scode, AllError.NotExistVoteUser)

        if selected and self.boardVoteUserRepository.insert(scode, userId, boardId, voteItemId) == False:
            return self.setError(scode, AllError.FailAddVoteUser)
        elif selected == False and self.boardVoteUserRepository.delete(scode, userId, boardId) == False:
            return self.setError(scode, AllError.FailDelVoteUser)

        if selected :
            self.boardVoteItemRepository.incVoteItem(scode, boardId, voteItemId)
        else:
            self.boardVoteItemRepository.decVoteItem(scode, boardId, voteItemId)

        voteItemList = self.boardVoteItemRepository.getVoteItemList(scode, boardId)
        return self.setOk(scode, {'boardId': boardId, 'voteItems': voteItemList})


    def updateVote(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']

        voteRec = self.boardVoteRepository.getVoteInfo(scode, boardId)
        if voteRec is None:
            return self.setError(scode, AllError.NotExistVoteInfo)
        elif voteRec['userId'] != userId:
            return self.setError(scode, AllError.PermissionDeny)
        elif voteRec['expiredAt'] < datetime.now() or voteRec['closed'] == True:
            return self.setError(scode, AllError.AlreadyExpired)

        if 'expiredAt' in jdata and jdata['expiredAt'] is not None:
            self.boardVoteRepository.updateExpireTime(scode, boardId, userId, jdata['expiredAt'])
        if 'closed' in jdata:
            self.boardVoteRepository.updateClose(scode, boardId, userId, jdata['closed'])
        if 'voteItems' in jdata and len(jdata['voteItems']) > 0:
            for voteItem in jdata['voteItems']:
                self.boardVoteItemRepository.updateVoteText(scode, boardId, voteItem['voteItemId'], voteItem['itemText'])
        return self.setOk(scode, boardId)

    def changeVoteSelection(self, scode, session, jdata):
        userId = session['userId']
        boardId = jdata['boardId']

        voteUser = self.boardVoteUserRepository.getVoteUser(scode, userId, boardId)
        if voteUser is None:
            return self.setError(scode, AllError.NotExistVoteUser)

        if voteUser['voteItemId'] == jdata['voteItemId']:
            return self.setError(scode, AllError.SelectSameVoteItem)

        if self.boardVoteUserRepository.updateSelectItem(scode, userId, boardId, jdata['voteItemId']) == False:
            return self.setError(scode, AllError.NotExistVoteInfo)
        self.boardVoteItemRepository.incVoteItem(scode, boardId, jdata['voteItemId'])
        self.boardVoteItemRepository.decVoteItem(scode, boardId, voteUser['voteItemId'])
        return self.setOk(scode, {'boardId': boardId, 'voteItemId': jdata['voteItemId']})

    def getVoteInfoList(self, scode, session, jdata):
        voteInfos = self.boardVoteRepository.getVoteInfoList(scode, jdata['boardIdds'])
        return self.setOk(scode, voteInfos)


 