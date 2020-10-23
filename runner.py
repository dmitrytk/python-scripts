def run(main):
    try:
        print('processing')
        main()
        input('Done!')
    except Exception as e:
        print(e)
        input()
