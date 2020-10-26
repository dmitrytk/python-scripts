def run(main):
    try:
        print('processing')
        main()
    except Exception as e:
        print(e)
        input()
