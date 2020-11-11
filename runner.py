def run(main):
    """Run main functions in scripts"""
    
    try:
        print('processing')
        main()
    except Exception as e:
        print(e)
        input()
